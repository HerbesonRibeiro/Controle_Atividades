import requests
import os
import sys
import tempfile
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox
from packaging import version


class GitHubUpdater:
    def __init__(self, repo_owner: str, repo_name: str, current_version: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.token = self._load_token()
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}' if self.token else None
        }

    def _load_token(self):
        """Carrega o token de forma segura"""
        # 1. Tenta variável de ambiente
        token = os.getenv('GITHUB_TOKEN')

        # 2. Tenta arquivo local (não versionado)
        if not token and os.path.exists('github_token.txt'):
            with open('github_token.txt', 'r') as f:
                token = f.read().strip()

        return token

    def check_for_updates(self) -> dict:
        """Verifica atualizações de forma robusta"""
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            release = response.json()

            latest_version = release['tag_name'].replace('v', '')
            return {
                'available': version.parse(latest_version) > version.parse(self.current_version),
                'version': latest_version,
                'notes': release.get('body', ''),
                'assets': release.get('assets', [])
            }
        except requests.exceptions.RequestException as e:
            return {'available': False, 'error': str(e)}

    def download_asset(self, asset_url: str) -> str:
        """Baixa o asset com tratamento de erros"""
        try:
            temp_dir = tempfile.mkdtemp()
            local_path = os.path.join(temp_dir, "update.zip")

            with requests.get(asset_url, headers=self.headers, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return local_path
        except Exception as e:
            raise Exception(f"Falha no download: {str(e)}")

    def apply_update(self, zip_path: str) -> bool:
        """Aplica a atualização de forma segura"""
        try:
            # Determina diretório alvo
            base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(
                os.path.abspath(__file__))

            # Extrai arquivos
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(base_dir)

            # Limpeza
            os.remove(zip_path)
            return True
        except Exception as e:
            raise Exception(f"Falha na aplicação: {str(e)}")

    def run_update_flow(self) -> bool:
        """Fluxo completo com UI"""
        update_info = self.check_for_updates()

        if not update_info.get('available'):
            return False

        # Mostra diálogo de confirmação
        root = tk.Tk()
        root.withdraw()

        user_response = messagebox.askyesno(
            "Atualização Disponível",
            f"Nova versão {update_info['version']} disponível!\n\n"
            f"Notas da versão:\n{update_info['notes']}\n\n"
            "Deseja instalar agora?"
        )

        if not user_response:
            return False

        try:
            # Encontra o primeiro asset .zip
            zip_asset = next(
                (asset for asset in update_info['assets']
                 if asset['name'].endswith('.zip')),
                None
            )

            if not zip_asset:
                raise Exception("Nenhum arquivo .zip encontrado nos assets")

            # Download e aplicação
            zip_path = self.download_asset(zip_asset['browser_download_url'])
            if self.apply_update(zip_path):
                messagebox.showinfo("Sucesso", "Atualização aplicada com sucesso! Reinicie o aplicativo.")
                return True

        except Exception as e:
            messagebox.showerror("Erro", f"Falha na atualização:\n{str(e)}")
            return False