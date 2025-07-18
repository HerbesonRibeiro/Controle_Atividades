# import tkinter as tk
# from screens.login_view import LoginView
#
# def main():
#     try:
#         root = tk.Tk()
#         root.geometry("400x300")
#         LoginView(root) # Só irá funcionar se a classe LoginView existir
#         root.mainloop()
#     except Exception as e:
#         print(f'Erro crítico: {e}')
#
# if __name__ == "__main__":
#     main()

import tkinter as tk
from screens.login_view import LoginView
import sys
import os
from GitHubUpdater import GitHubUpdater  # Importe do arquivo correto


def check_updates():
    """Verifica e aplica atualizações de forma segura"""
    try:
        # Configuração do updater - substitua com seus dados
        updater = GitHubUpdater(
            repo_owner="SEU_USUARIO_GITHUB",
            repo_name="SEU_REPOSITORIO",
            current_version="1.0.0"  # Atualize conforme sua versão
        )

        # Verifica sem mostrar erros ao usuário final
        update_info = updater.check_for_updates()

        if update_info.get('available'):
            # Mostra diálogo de confirmação
            root = tk.Tk()
            root.withdraw()  # Esconde a janela principal

            resposta = tk.messagebox.askyesno(
                "Atualização Disponível",
                f"Versão {update_info['latest_version']} disponível!\n\n"
                f"Notas da versão:\n{update_info['release_notes']}\n\n"
                "Deseja instalar agora?",
                parent=root
            )

            if resposta:
                if updater.perform_update():
                    root.destroy()
                    return True

            root.destroy()

    except Exception as e:
        print(f"[Updater] Erro silencioso: {str(e)}")
    return False


def main():
    # Verifica atualizações antes de iniciar
    if check_updates():
        # Reinicia a aplicação se atualizou
        python = sys.executable
        os.execl(python, python, *sys.argv)

    try:
        root = tk.Tk()
        root.geometry("400x300")
        root.title("Seu Aplicativo")  # Adicione um título

        # Adiciona ícone (opcional)
        try:
            root.iconbitmap('app_icon.ico')  # Substitua pelo seu ícone
        except:
            pass

        LoginView(root)
        root.mainloop()

    except Exception as e:
        tk.messagebox.showerror(
            "Erro Inesperado",
            f"O aplicativo encontrou um erro e será fechado:\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()