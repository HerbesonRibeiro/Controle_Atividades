import os
import sys
import logging
import tkinter as tk
from tkinter import messagebox
from screens.login_view import LoginView
from GitHubUpdater import GitHubUpdater
from dotenv import load_dotenv
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def resource_path(relative_path):
    """Retorna o caminho absoluto do recurso, adaptado ao modo .exe do PyInstaller."""
    try:
        base_path = sys._MEIPASS  # pasta temporária usada pelo PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # modo desenvolvimento
    return os.path.join(base_path, relative_path)

# Carrega e descriptografa variáveis do .env
load_dotenv(resource_path(".env"))

# Descriptografa o GITHUB_TOKEN
try:
    raw_token = os.getenv("GITHUB_TOKEN", "").encode()
    key = os.getenv("KEY", "").encode()
    github_token = Fernet(key).decrypt(raw_token).decode()
except Exception as e:
    logger.warning(f"🔐 Falha ao descriptografar GITHUB_TOKEN: {e}")
    github_token = None

def check_updates():
    try:
        updater = GitHubUpdater(
            repo_owner="HerbesonRibeiro",
            repo_name="Controle_Atividades",
            current_version="1.0.0",
            token=github_token
        )
        update_info = updater.check_for_updates()
        if update_info.get('available'):
            root = tk.Tk()
            root.withdraw()
            resposta = messagebox.askyesno(
                "Atualização Disponível",
                f"Versão {update_info['latest_version']} disponível!\n\n"
                f"Notas da versão:\n{update_info['release_notes']}\n\n"
                "Deseja instalar agora?",
                parent=root
            )
            root.destroy()
            if resposta and updater.perform_update():
                return True
    except Exception as e:
        logger.debug(f"[Updater] Erro silencioso: {e}")
    return False

def main():
    if check_updates():
        python = sys.executable
        os.execl(python, python, *sys.argv)
    try:
        root = tk.Tk()
        root.geometry("400x300")
        root.title("Controle de Atividades")
        try:
            root.iconbitmap(resource_path("assets/icon.ico"))
        except:
            pass
        LoginView(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"O aplicativo encontrou um erro e será fechado:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()