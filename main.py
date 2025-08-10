#
# import os
# import sys
# import json
# import threading
# import logging
# import inspect
# import ctypes  # só no Windows para AppUserModelID
# import tkinter as tk
# from tkinter import messagebox
# from dotenv import load_dotenv
#
# # Import do updater e da view do login (ajuste paths se necessário)
# from GitHubUpdater import GitHubUpdater
# from screens.login_view import LoginView
#
# # ============================
# # Configuração de logging
# # ============================
# logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
# logger = logging.getLogger(__name__)
#
# # ============================
# # Utils
# # ============================
# def resource_path(relative_path: str) -> str:
#     """
#     Caminho compatível com PyInstaller.
#     Use resource_path("assets/icon.ico") para carregar arquivos empacotados.
#     """
#     try:
#         base_path = sys._MEIPASS
#     except AttributeError:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)
#
# def get_current_version(default="1.0.4") -> str:
#     """
#     Tenta ler version.json na raiz (sempre útil para PyUpdater).
#     Espera um JSON: { "version": "1.0.3" }
#     """
#     try:
#         p = resource_path("version.json")
#         if os.path.exists(p):
#             with open(p, "r", encoding="utf-8") as fh:
#                 data = json.load(fh)
#             v = data.get("version")
#             if v:
#                 return v
#     except Exception as e:
#         logger.debug("Não foi possível ler version.json: %s", e)
#     return default
#
# # ============================
# # Carregamento .env e token
# # ============================
# load_dotenv(resource_path(".env"))
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# if not GITHUB_TOKEN:
#     logger.warning("⚠️ GITHUB_TOKEN não definido no .env — atualizações podem falhar para repositórios privados.")
#
# # ============================
# # Controle de concorrência do updater
# # ============================
# _update_lock = threading.Lock()
# _update_dialog_shown = False
# _update_in_progress = False
#
# def _run_update_in_thread(updater: GitHubUpdater):
#     """
#     Função que roda dentro da thread para baixar/aplicar/reiniciar.
#     """
#     try:
#         logger.info("[Updater] Thread de atualização iniciada.")
#         zip_path = updater._download_update(updater.check_for_updates().get("assets", []))
#         if not zip_path:
#             logger.error("[Updater] Nenhum arquivo de atualização foi baixado.")
#             return False
#
#         applied = updater._apply_update(zip_path)
#         if applied:
#             logger.info("[Updater] Atualização aplicada. Reiniciando...")
#             updater._restart_app()
#             return True
#         else:
#             logger.error("[Updater] Falha ao aplicar atualização.")
#             return False
#     except Exception:
#         logger.exception("[Updater] Erro na thread de atualização.")
#         return False
#
# def check_updates(parent_root=None, current_version=None):
#     """
#     Verifica atualizações no GitHub, protegendo contra chamadas concorrentes e
#     evitando mostrar o diálogo mais de uma vez.
#     parent_root: instância Tk para associar o messagebox (opcional)
#     """
#     global _update_dialog_shown, _update_in_progress
#
#     if current_version is None:
#         current_version = get_current_version()
#
#     # Proteção contra concorrência
#     with _update_lock:
#         if _update_dialog_shown:
#             logger.debug("[Updater] Diálogo já mostrado — pulando verificação.")
#             return False
#         if _update_in_progress:
#             # Log da stack do chamador para debug - Apenas para devolver a URL
#             stack = "".join(inspect.format_stack(limit=6))
#             logger.debug("[Updater] Outra checagem em andamento. Stack do chamador:\n%s", stack)
#             return False
#         _update_in_progress = True
#
#     try:
#         if not GITHUB_TOKEN:
#             logger.info("[Updater] Token ausente — tentando checar releases públicos.")
#         updater = GitHubUpdater(
#             repo_owner="HerbesonRibeiro",
#             repo_name="Controle_Atividades",
#             current_version=current_version,
#             token=GITHUB_TOKEN
#         )
#
#         info = updater.check_for_updates()
#     except Exception:
#         logger.exception("[Updater] Falha ao checar atualizações.")
#         info = {"available": False}
#     finally:
#         # libera o in_progress (o diálogo marcado só após confirmar disponibilidade)
#         with _update_lock:
#             _update_in_progress = False
#
#     if not info.get("available"):
#         logger.debug("[Updater] Nenhuma atualização disponível.")
#         return False
#
#     # marca que o diálogo será mostrado para evitar repetições
#     with _update_lock:
#         if _update_dialog_shown:
#             logger.debug("[Updater] Outro fluxo já marcou diálogo; abortando.")
#             return False
#         _update_dialog_shown = True
#
#     # Mostra diálogo para o usuário (usa parent_root se fornecido)
#     temp_parent = False
#     parent = parent_root
#     if parent is None:
#         parent = tk.Tk()
#         parent.withdraw()
#         temp_parent = True
#
#     resposta = messagebox.askyesno(
#         "Atualização Disponível",
#         f"Versão {info['latest_version']} disponível!\n\n"
#         f"Notas da versão:\n{info.get('release_notes','')}\n\n"
#         "Deseja instalar agora?",
#         parent=parent
#     )
#
#     if temp_parent:
#         parent.destroy()
#
#     if not resposta:
#         logger.info("[Updater] Usuário recusou atualização.")
#         return False
#
#     # inicia download/aplicação em background
#     try:
#         thread = threading.Thread(target=_run_update_in_thread, args=(updater,), daemon=True)
#         thread.start()
#         logger.info("[Updater] Atualização iniciada em background.")
#         return True
#     except Exception:
#         logger.exception("[Updater] Falha ao iniciar thread de atualização.")
#         return False
#
# # ============================
# # InactivityManager
# # ============================
# class InactivityManager:
#     def __init__(self, root, timeout_ms=10*60*1000):  # 10 minutos
#         self.root = root
#         self.timeout_ms = timeout_ms
#         self._after_id = None
#         self.root.bind_all("<Motion>", self.reset_timer)
#         self.root.bind_all("<Key>", self.reset_timer)
#         self.start_timer()
#
#     def start_timer(self):
#         self._after_id = self.root.after(self.timeout_ms, self.shutdown)
#
#     def reset_timer(self, event=None):
#         if self._after_id:
#             self.root.after_cancel(self._after_id)
#         self.start_timer()
#
#     def shutdown(self):
#         logger.info("⏳ Encerrando o sistema por inatividade...")
#         try:
#             self.root.destroy()
#         except Exception:
#             pass
#         sys.exit(0)
#
# # ============================
# # Main
# # ============================
# def main():
#     # Define AppUserModelID no Windows (melhora ícone na barra)
#     if sys.platform.startswith("win"):
#         try:
#             myappid = "com.seuprojeto.controleatividades"
#             ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
#         except Exception:
#             logger.debug("Não foi possível setar AppUserModelID.")
#
#     try:
#         root = tk.Tk()
#         root.geometry("400x300")
#         root.title("Controle de Atividades")
#
#         # Ícone
#         try:
#             root.iconbitmap(resource_path("assets/icon.ico"))
#         except Exception:
#             logger.debug("Ícone não encontrado ou não pode ser carregado.")
#
#         # Gerenciador de inatividade (opcional)
#         InactivityManager(root)
#
#         # Checa atualizações uma vez, em 1s (não bloqueante)
#         root.after(1000, lambda: check_updates(parent_root=root))
#
#         # Mostra a tela de login (sua implementação)
#         LoginView(root)
#
#         root.mainloop()
#     except Exception as e:
#         # Em caso de erro crítico, mostra mensagem ao usuário
#         try:
#             messagebox.showerror("Erro Inesperado", f"O aplicativo encontrou um erro e será fechado:\n\n{e}")
#         except Exception:
#             logger.exception("Erro fatal antes de exibir dialog.")
#         sys.exit(1)
#
# if __name__ == "__main__":
#     main()

import os
import sys
import json
import threading
import logging
import inspect
import ctypes  # só no Windows para AppUserModelID
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# Import do updater e da view do login (ajuste paths se necessário)
from GitHubUpdater import GitHubUpdater
from screens.login_view import LoginView

# ============================
# Configuração de logging
# ============================
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


# ============================
# Utils
# ============================
def resource_path(relative_path: str) -> str:
    """
    Caminho compatível com PyInstaller.
    Use resource_path("assets/icon.ico") para carregar arquivos empacotados.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_current_version(default="1.0.4") -> str:
    """
    Tenta ler version.json na raiz (sempre útil para PyUpdater).
    Espera um JSON: { "version": "1.0.3" }
    """
    try:
        p = resource_path("version.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            v = data.get("version")
            if v:
                return v
    except Exception as e:
        logger.debug("Não foi possível ler version.json: %s", e)
    return default


# ============================
# Carregamento .env e token
# ============================
load_dotenv(resource_path(".env"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    logger.warning("⚠️ GITHUB_TOKEN não definido no .env — atualizações podem falhar para repositórios privados.")

# ============================
# Controle de concorrência do updater
# ============================
_update_lock = threading.Lock()
_update_dialog_shown = False
_update_in_progress = False


def _run_update_in_thread(updater: GitHubUpdater):
    """
    Função que roda dentro da thread para baixar/aplicar/reiniciar.
    """
    try:
        logger.info("[Updater] Thread de atualização iniciada.")
        zip_path = updater._download_update(updater.check_for_updates().get("assets", []))
        if not zip_path:
            logger.error("[Updater] Nenhum arquivo de atualização foi baixado.")
            return False

        applied = updater._apply_update(zip_path)
        if applied:
            logger.info("[Updater] Atualização aplicada. Reiniciando...")
            updater._restart_app()
            return True
        else:
            logger.error("[Updater] Falha ao aplicar atualização.")
            return False
    except Exception:
        logger.exception("[Updater] Erro na thread de atualização.")
        return False


def check_updates(parent_root=None, current_version=None):
    """
    Verifica atualizações no GitHub, protegendo contra chamadas concorrentes e
    evitando mostrar o diálogo mais de uma vez.
    parent_root: instância Tk para associar o messagebox (opcional)
    """
    global _update_dialog_shown, _update_in_progress

    if current_version is None:
        current_version = get_current_version()

    with _update_lock:
        if _update_dialog_shown:
            logger.debug("[Updater] Diálogo já mostrado — pulando verificação.")
            return False
        if _update_in_progress:
            stack = "".join(inspect.format_stack(limit=6))
            logger.debug("[Updater] Outra checagem em andamento. Stack do chamador:\n%s", stack)
            return False
        _update_in_progress = True

    try:
        if not GITHUB_TOKEN:
            logger.info("[Updater] Token ausente — tentando checar releases públicos.")
        updater = GitHubUpdater(
            repo_owner="HerbesonRibeiro",
            repo_name="Controle_Atividades",
            current_version=current_version,
            token=GITHUB_TOKEN
        )
        info = updater.check_for_updates()
    except Exception:
        logger.exception("[Updater] Falha ao checar atualizações.")
        info = {"available": False}
    finally:
        with _update_lock:
            _update_in_progress = False

    if not info.get("available"):
        logger.debug("[Updater] Nenhuma atualização disponível.")
        return False

    with _update_lock:
        if _update_dialog_shown:
            logger.debug("[Updater] Outro fluxo já marcou diálogo; abortando.")
            return False
        _update_dialog_shown = True

    temp_parent = False
    parent = parent_root
    if parent is None:
        parent = tk.Tk()
        parent.withdraw()
        temp_parent = True

    resposta = messagebox.askyesno(
        "Atualização Disponível",
        f"Versão {info['latest_version']} disponível!\n\n"
        f"Notas da versão:\n{info.get('release_notes', '')}\n\n"
        "Deseja instalar agora?",
        parent=parent
    )
    if temp_parent: parent.destroy()

    if not resposta:
        logger.info("[Updater] Usuário recusou atualização.")
        return False

    try:
        thread = threading.Thread(target=_run_update_in_thread, args=(updater,), daemon=True)
        thread.start()
        logger.info("[Updater] Atualização iniciada em background.")
        return True
    except Exception:
        logger.exception("[Updater] Falha ao iniciar thread de atualização.")
        return False


# ============================
# InactivityManager
# ============================
class InactivityManager:
    def __init__(self, root, timeout_ms=10 * 60 * 1000):  # 10 minutos
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
        try:
            self.root.destroy()
        except Exception:
            pass
        sys.exit(0)


# ============================
# Main
# ============================
def main():
    if sys.platform.startswith("win"):
        try:
            myappid = "com.seuprojeto.controleatividades"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            logger.debug("Não foi possível setar AppUserModelID.")

    try:
        root = tk.Tk()
        root.geometry("400x300")
        root.title("Controle de Atividades")

        try:
            root.iconbitmap(resource_path("assets/icon.ico"))
        except Exception:
            logger.debug("Ícone não encontrado ou não pode ser carregado.")

        # <<< CORREÇÃO >>>: Funcionalidade de fechar por inatividade foi desativada.
        # Gerenciador de inatividade (opcional)
        # InactivityManager(root)

        root.after(1000, lambda: check_updates(parent_root=root))
        LoginView(root)
        root.mainloop()

    except Exception as e:
        try:
            messagebox.showerror("Erro Inesperado", f"O aplicativo encontrou um erro e será fechado:\n\n{e}")
        except Exception:
            logger.exception("Erro fatal antes de exibir dialog.")
        sys.exit(1)


if __name__ == "__main__":
    main()