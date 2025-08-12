# VERSÃO FINAL, SIMPLES E ROBUSTA
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


class GitHubUpdater:
    def __init__(self, repo_owner: str, repo_name: str, current_version: str, token: str = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.token = token or self._load_token_if_present()

    def _load_token_if_present(self):
        try:
            load_dotenv()
            return os.getenv("GITHUB_TOKEN")
        except Exception:
            return None

    def check_for_updates(self):
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
            logger.error("Erro na API do GitHub: %s - %s", resp.status_code, resp.text)
            return {'available': False}

        release = resp.json()
        latest_version = release.get("tag_name", "").lstrip("v")
        is_newer = False
        try:
            is_newer = version.parse(latest_version) > version.parse(self.current_version)
        except Exception:
            logger.exception("Falha ao comparar versões: %s vs %s", latest_version, self.current_version)

        return {'available': is_newer, 'latest_version': latest_version, 'release_notes': release.get('body', ''),
                'assets': release.get('assets', [])}

    def _download_update(self, assets):
        for asset in assets:
            name = asset.get("name", "")
            if name.endswith(".zip"):
                download_url = asset.get("browser_download_url")
                if not download_url: continue
                try:
                    resp = requests.get(download_url, stream=True, timeout=120)
                    if resp.status_code == 200:
                        temp_dir = tempfile.mkdtemp()
                        zip_path = os.path.join(temp_dir, name)
                        with open(zip_path, "wb") as f:
                            shutil.copyfileobj(resp.raw, f)
                        return zip_path
                    else:
                        logger.error(f"Falha no download. Status: {resp.status_code}")
                except requests.RequestException as e:
                    logger.exception(f"Erro de rede durante o download: {e}")
        return None

    def _apply_update(self, zip_path):
        try:
            current_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(
                os.path.abspath(__file__))
            temp_extract_dir = tempfile.mkdtemp()

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)

            exe_name = os.path.basename(sys.executable).lower() if getattr(sys, 'frozen', False) else None

            for root_dir, _, files in os.walk(temp_extract_dir):
                for file in files:
                    if exe_name and file.lower() == exe_name:
                        continue
                    src_path = os.path.join(root_dir, file)
                    rel_path = os.path.relpath(src_path, temp_extract_dir)
                    dst_path = os.path.join(current_dir, rel_path)
                    try:
                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                        shutil.copy2(src_path, dst_path)
                    except Exception as copy_error:
                        logger.exception(f"FALHA AO COPIAR o arquivo '{rel_path}': {copy_error}")
                        return False
            return True
        except Exception as e:
            logger.exception(f"Erro fatal durante a aplicação da atualização: {e}")
            return False

    def _restart_app(self):
        try:
            if getattr(sys, 'frozen', False):
                os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            logger.exception(f"Falha ao reiniciar: {e}")

    def run_update_flow(self, update_info=None):
        if update_info is None:
            update_info = self.check_for_updates()
        if not update_info or not update_info.get('available'):
            return False

        release_notes = update_info.get('release_notes')
        if not release_notes or not release_notes.strip():
            release_notes = "Nenhuma novidade descrita para esta versão."

        message = (
            f"Uma nova versão ({update_info['latest_version']}) está disponível!\n\n"
            f"O que há de novo:\n"
            f"--------------------------\n"
            f"{release_notes}\n"
            f"--------------------------\n\n"
            f"Deseja baixar e instalar a atualização agora?"
        )

        root = Tk()
        root.withdraw()
        if not messagebox.askyesno("Atualização Disponível", message, parent=root):
            root.destroy()
            return False

        # O programa vai "congelar" aqui durante o download e aplicação, o que é o comportamento esperado.
        zip_path = self._download_update(update_info.get('assets', []))
        if not zip_path:
            messagebox.showerror("Erro", "Falha no download da atualização.", parent=root)
            root.destroy()
            return False

        if not self._apply_update(zip_path):
            messagebox.showerror("Erro", "Não foi possível aplicar a atualização.", parent=root)
            root.destroy()
            return False

        messagebox.showinfo("Atualização Concluída", "O programa foi atualizado e será reiniciado agora.", parent=root)
        root.destroy()
        self._restart_app()
        return True