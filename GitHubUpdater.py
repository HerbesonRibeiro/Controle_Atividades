import os
import sys
import requests
import zipfile
import shutil
import tempfile
import logging
from tkinter import messagebox, Tk
from packaging import version
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class GitHubUpdater:
    def __init__(self, repo_owner: str, repo_name: str, current_version: str, token: str = None):
        """
        token: opcional. Se não informado, será carregado do .env (GITHUB_TOKEN).
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.token = token or self._load_token_if_present()

    def _load_token_if_present(self):
        """Carrega token puro do .env se existir (não tenta descriptografar)."""
        try:
            load_dotenv()
            token = os.getenv("GITHUB_TOKEN")
            return token
        except Exception:
            return None

    def check_for_updates(self):
        """Verifica se existe release mais nova no GitHub."""
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        headers = {"User-Agent": "ControleAtividades-Updater/1.0"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        try:
            resp = requests.get(url, headers=headers, timeout=30)
        except requests.RequestException as e:
            logger.exception("Erro de rede ao verificar atualizações: %s", e)
            return {'available': False}

        if resp.status_code != 200:
            logger.error("Erro ao verificar atualização: %s - %s", resp.status_code, resp.text)
            return {'available': False}

        release = resp.json()
        latest_version = release.get("tag_name", "").lstrip("v")
        is_newer = False
        try:
            is_newer = version.parse(latest_version) > version.parse(self.current_version)
        except Exception:
            logger.exception("Falha ao comparar versões: %s vs %s", latest_version, self.current_version)

        return {
            'available': is_newer,
            'latest_version': latest_version,
            'release_notes': release.get('body', ''),
            'assets': release.get('assets', [])
        }

    def _download_update(self, assets):
        """Baixa o .zip do release. Tenta com token (se houver), e se falhar
           com 401/403/404 tenta sem token (quando release é público)."""
        for asset in assets:
            name = asset.get("name", "")
            if not name.endswith(".zip"):
                continue

            download_url = asset.get("browser_download_url")
            if not download_url:
                logger.error("Asset sem browser_download_url: %s", asset)
                continue

            logger.info("Tentando baixar asset: %s", download_url)
            headers = {"User-Agent": "ControleAtividades-Updater/1.0", "Accept": "application/octet-stream"}
            if self.token:
                headers["Authorization"] = f"token {self.token}"

            try:
                resp = requests.get(download_url, headers=headers, stream=True, timeout=60)
                logger.debug("Resposta do download: %s", resp.status_code)
                if resp.status_code == 200:
                    temp_dir = tempfile.mkdtemp()
                    zip_path = os.path.join(temp_dir, name)
                    with open(zip_path, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    logger.info("Download concluído: %s", zip_path)
                    return zip_path

                # Se foi 401/403/404 e havia token, tenta sem token (caso público)
                if resp.status_code in (401, 403, 404) and self.token:
                    logger.warning("Falha autenticada (%s). Tentando sem token...", resp.status_code)
                    headers.pop("Authorization", None)
                    resp2 = requests.get(download_url, headers=headers, stream=True, timeout=60)
                    logger.debug("Resposta tentativa sem token: %s", resp2.status_code)
                    if resp2.status_code == 200:
                        temp_dir = tempfile.mkdtemp()
                        zip_path = os.path.join(temp_dir, name)
                        with open(zip_path, "wb") as f:
                            for chunk in resp2.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        logger.info("Download concluído (sem token): %s", zip_path)
                        return zip_path

                logger.error("Erro ao baixar atualização: %s", resp.status_code)
            except requests.RequestException as e:
                logger.exception("Erro HTTP ao tentar baixar asset: %s", e)

        return None

    def _apply_update(self, zip_path):
        current_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        temp_extract_dir = tempfile.mkdtemp()

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)
        except zipfile.BadZipFile:
            logger.exception("Arquivo zip inválido: %s", zip_path)
            return False

        # Nome do exe atual em execução
        exe_name = os.path.basename(sys.executable) if getattr(sys, 'frozen', False) else None

        for root_dir, _, files in os.walk(temp_extract_dir):
            for file in files:
                if exe_name and file.lower() == exe_name.lower():
                    logger.info(f"Pulei o executável em uso: {file}")
                    continue  # NÃO substitua o exe em uso

                src_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(src_path, temp_extract_dir)
                dst_path = os.path.join(current_dir, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

        logger.info(
            "Arquivos atualizados, mas executável permanece o mesmo. Reinicie o programa para aplicar a atualização.")
        return True

    def _restart_app(self):
        if getattr(sys, 'frozen', False):
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            os.execlp("python", "python", *sys.argv)

    def run_update_flow(self, update_info=None):
        """Fluxo de atualização. Se update_info já existe, usa-o (evita re-checar)."""
        if update_info is None:
            update_info = self.check_for_updates()
        if not update_info or not update_info.get('available'):
            return False

        root = Tk()
        root.withdraw()
        resposta = messagebox.askyesno(
            "Atualização disponível",
            f"Versão {update_info['latest_version']} disponível!\n\n"
            f"Notas da versão:\n{update_info['release_notes']}\n\n"
            "Deseja atualizar agora?"
        )
        root.destroy()

        if not resposta:
            return False

        zip_path = self._download_update(update_info.get('assets', []))
        if not zip_path:
            logger.error("Nenhum arquivo de atualização foi baixado.")
            return False

        if not self._apply_update(zip_path):
            logger.error("Falha ao aplicar a atualização.")
            return False

        logger.info("Atualização aplicada. Reiniciando...")
        self._restart_app()
        return True

    def perform_update(self, update_info=None):
        """Alias usado por main.py — passe update_info para evitar nova checagem."""
        return self.run_update_flow(update_info)
