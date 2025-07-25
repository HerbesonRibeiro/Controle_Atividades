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
    try:
        base_path = sys._MEIPASS  # usado no executável
    except AttributeError:
        base_path = os.path.abspath(".")  # usado em modo desenvolvimento
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
            current_version="1.0.1",
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

# ✅ Classe para controle de inatividade global
class InactivityManager:
    def __init__(self, root, timeout_ms=10*60*1000):  # 10 minutos
        self.root = root
        self.timeout_ms = timeout_ms
        self._after_id = None
        self.root.bind_all("<Motion>", self.reset_timer)
        self.root.bind_all("<Key>", self.reset_timer)
        self.start_timer()

    def start_timer(self):
        self._after_id = self.root.after(self.timeout_ms, self.shutdown)

    def reset_timer(self, event=None):
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self.start_timer()

    def shutdown(self):
        logger.info("⏳ Encerrando o sistema por inatividade...")
        self.root.destroy()
        sys.exit(0)

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
        except Exception as e:
            logger.warning(f"⚠️ Erro ao definir ícone: {e}")

        # ✅ Ativa o controle de inatividade global
        InactivityManager(root)

        LoginView(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"O aplicativo encontrou um erro e será fechado:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
