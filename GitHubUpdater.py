# GitHubUpdater.py
import requests
import os
import sys
import tempfile
import zipfile
import shutil
import tk
from packaging import version
import tkinter.messagebox as msgbox


class GitHubUpdater:
    def __init__(self, repo_owner: str, repo_name: str, current_version: str):
        """
        :param repo_owner: Seu usuário GitHub (ex: 'seunome')
        :param repo_name: Nome do repositório (ex: 'meu-app')
        :param current_version: Versão atual (ex: '1.0.0')
        """
        self.repo_owner = repo_owner = "HerbesonRibeiro"
        self.repo_name = repo_name = "Controle_atividades"
        self.current_version = current_version = "1.0.0"
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}

    def check_for_updates(self) -> dict:
        """Verifica atualizações no GitHub"""
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            release = response.json()

            latest_version = release['tag_name'].lstrip('v')
            if version.parse(latest_version) > version.parse(self.current_version):
                return {
                    'available': True,
                    'version': latest_version,
                    'notes': release.get('body', ''),
                    'assets': release.get('assets', [])
                }
            return {'available': False}

        except Exception as e:
            print(f"[Updater] Erro: {str(e)}")
            return {'available': False, 'error': str(e)}

    def download_asset(self, url: str) -> str:
        """Baixa o arquivo de atualização"""
        try:
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, "update.zip")

            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return file_path

        except Exception as e:
            print(f"[Updater] Download falhou: {str(e)}")
            raise

    def apply_update(self, zip_path: str) -> bool:
        """Extrai e aplica a atualização"""
        try:
            # 1. Criar backup
            backup_dir = os.path.join(tempfile.gettempdir(), f"{self.repo_name}_backup")
            os.makedirs(backup_dir, exist_ok=True)

            # 2. Copiar arquivos existentes
            for item in os.listdir('.'):
                if item.endswith('.py') or item.endswith('.exe'):
                    shutil.copy2(item, backup_dir)

            # 3. Extrair novos arquivos
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('.')

            return True

        except Exception as e:
            print(f"[Updater] Falha na aplicação: {str(e)}")
            # Restaurar backup se necessário
            return False

    def run_update_flow(self) -> bool:
        """Executa todo o fluxo de atualização"""
        update_info = self.check_for_updates()
        if not update_info.get('available'):
            return False

        # Mostrar diálogo de confirmação
        root = tk.Tk()
        root.withdraw()
        answer = msgbox.askyesno(
            "Atualização Disponível",
            f"Versão {update_info['version']} disponível!\n\n"
            f"Notas da versão:\n{update_info['notes']}\n\n"
            "Deseja instalar agora? (O aplicativo será reiniciado)"
        )
        root.destroy()

        if not answer:
            return False

        try:
            asset_url = next(
                (asset['browser_download_url']
                 for asset in update_info['assets']
                 if asset['name'].endswith('.zip')),
                None
            )

            if not asset_url:
                msgbox.showerror("Erro", "Arquivo de atualização não encontrado!")
                return False

            zip_path = self.download_asset(asset_url)
            if self.apply_update(zip_path):
                msgbox.showinfo("Sucesso", "Atualização aplicada com sucesso! Reiniciando...")
                return True

        except Exception as e:
            msgbox.showerror("Erro", f"Falha na atualização:\n{str(e)}")
            return False