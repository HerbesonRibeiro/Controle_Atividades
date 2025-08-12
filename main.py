# VERSÃO FINAL DE PRODUÇÃO
import tkinter as tk
from screens.login_view import LoginView
from screens.home_view import HomeView
import logging
import sys
from pathlib import Path
import ctypes
import json
import threading
from GitHubUpdater import GitHubUpdater

# --- Lógica de Versão Centralizada ---
APP_NAME = "controle-atividades"
__version__ = "0.0.0"


def get_base_path():
    """Retorna o caminho base do executável de forma robusta."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent


def load_version():
    """Carrega a versão do arquivo version.json."""
    global __version__
    try:
        version_path = get_base_path() / "version.json"
        with open(version_path, 'r') as f:
            data = json.load(f)
        __version__ = str(data.get("version", __version__))
    except Exception:
        pass  # Em produção, se falhar, usa a versão padrão silenciosamente


class App:
    def __init__(self, master):
        self.master = master
        try:
            myappid = f'herbeson.{APP_NAME}.{__version__}'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except AttributeError:
            pass

        self._configure_window_icon(self.master)
        self.master.withdraw()

        self.current_window = None
        self.colaborador = None

        self.check_for_updates_in_background()
        self.show_login_window()

    def _configure_window_icon(self, window):
        try:
            icon_path = get_base_path() / "assets" / "icon.ico"
            if icon_path.exists(): window.iconbitmap(default=icon_path)
        except Exception:
            pass  # Falha silenciosa em produção

    def check_for_updates_in_background(self):
        """Inicia a verificação de atualização em uma thread separada."""
        updater = GitHubUpdater(
            repo_owner="HerbesonRibeiro",
            repo_name="Controle_Atividades",
            current_version=__version__
        )
        thread = threading.Thread(target=updater.run_update_flow, daemon=True)
        thread.start()

    def show_login_window(self):
        if self.current_window: self.current_window.destroy()
        self.current_window = tk.Toplevel(self.master)
        self.login_view = LoginView(self.current_window, self.on_login_success)
        self.current_window.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def show_home_window(self):
        if self.current_window: self.current_window.destroy()
        self.current_window = tk.Toplevel(self.master)
        self.home_view = HomeView(self.current_window, self.colaborador, self.on_logout)
        self.current_window.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def on_login_success(self, colaborador):
        self.colaborador = colaborador
        self.show_home_window()

    def on_logout(self):
        self.colaborador = None
        self.show_login_window()


if __name__ == "__main__":
    load_version()
    # Configuração de log mínima para produção
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")

    root = tk.Tk()
    app = App(root)
    root.mainloop()