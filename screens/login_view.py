import tkinter as tk
from tkinter import ttk, messagebox
import logging
import json
import os
from controllers.auth_controller import AuthController

CAMINHO_USUARIO_SALVO = "ultimo_usuario.json"

class LoginView:
    def __init__(self, master):
        self.master = master
        self.controller = AuthController()

        self.master.title("Controle de Atividades")
        self.master.geometry("380x340")
        self.master.resizable(False, False)
        self.master.configure(bg='#f8f9fa')
        self.master.eval('tk::PlaceWindow . center')

        self._setup_ui()
        self._carregar_usuario_salvo()

    def _setup_ui(self):
        self.main_frame = tk.Frame(self.master, bg='#f8f9fa', padx=30, pady=20)
        self.main_frame.pack(expand=True, fill='both')

        # Removida a parte que carrega a imagem
        # Agora só título em texto
        tk.Label(self.main_frame, text="Controle de Atividades",
                 font=('Segoe UI', 16, 'bold'), bg='#f8f9fa', fg='#343a40').pack(pady=(0, 20))

        # Campo usuário
        tk.Label(self.main_frame, text="Usuário", bg='#f8f9fa', fg='#495057',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        self.ent_usuario = tk.Entry(self.main_frame, font=('Segoe UI', 10), bd=1, relief='solid')
        self.ent_usuario.pack(fill='x', pady=(0, 10), ipady=5)

        # Checkbutton para lembrar usuário
        self.var_lembrar = tk.BooleanVar()
        tk.Checkbutton(self.main_frame, text="Lembrar usuário", variable=self.var_lembrar,
                       bg='#f8f9fa', font=('Segoe UI', 9)).pack(anchor='w', pady=(0, 10))

        # Campo senha
        tk.Label(self.main_frame, text="Senha", bg='#f8f9fa', fg='#495057',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        senha_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        senha_frame.pack(fill='x')

        self.ent_senha = tk.Entry(senha_frame, font=('Segoe UI', 10), bd=1, relief='solid', show="•")
        self.ent_senha.pack(side='left', fill='x', expand=True, ipady=5)

        self.btn_show_pwd = tk.Button(
            senha_frame, text="👁", width=3, command=self._toggle_password,
            bg='#dee2e6', bd=0, relief='flat', activebackground='#ced4da'
        )
        self.btn_show_pwd.pack(side='right', padx=(5, 0))

        # Botão login
        self.btn_login = tk.Button(
            self.main_frame,
            text="Entrar",
            command=self._on_login,
            bg='#4e73df', fg='white',
            font=('Segoe UI', 10, 'bold'),
            activebackground='#375aba',
            bd=0, height=2
        )
        self.btn_login.pack(fill='x', pady=(20, 10))

        tk.Label(self.main_frame, text="Esqueceu a senha?",
                 fg="#6c757d", bg='#f8f9fa',
                 font=('Segoe UI', 9, 'underline'),
                 cursor="hand2").pack()

        self.master.bind_all('<Return>', self._login_handler)

    def _carregar_usuario_salvo(self):
        if os.path.exists(CAMINHO_USUARIO_SALVO):
            try:
                with open(CAMINHO_USUARIO_SALVO, 'r') as f:
                    dados = json.load(f)
                    usuario = dados.get("usuario")
                    if usuario:
                        self.ent_usuario.insert(0, usuario)
                        self.var_lembrar.set(True)
            except Exception as e:
                logging.warning(f"Erro ao carregar último usuário salvo: {e}")

    def _salvar_usuario(self):
        if self.var_lembrar.get():
            try:
                with open(CAMINHO_USUARIO_SALVO, 'w') as f:
                    json.dump({"usuario": self.ent_usuario.get().strip()}, f)
            except Exception as e:
                logging.warning(f"Erro ao salvar usuário: {e}")
        else:
            if os.path.exists(CAMINHO_USUARIO_SALVO):
                os.remove(CAMINHO_USUARIO_SALVO)

    def _login_handler(self, event):
        try:
            if self.master.winfo_exists():
                self._on_login()
        except:
            pass

    def _toggle_password(self):
        if self.ent_senha.cget('show') == '•':
            self.ent_senha.config(show='')
            self.btn_show_pwd.config(text='🚫')
        else:
            self.ent_senha.config(show='•')
            self.btn_show_pwd.config(text='👁')

    def _on_login(self):
        try:
            usuario = self.ent_usuario.get().strip()
            senha = self.ent_senha.get().strip()

            if not usuario or not senha:
                raise ValueError("Preencha todos os campos")

            self.btn_login.config(state=tk.DISABLED, text="Autenticando...")
            self.master.config(cursor="wait")
            self.master.update()

            colaborador = self.controller.autenticar(usuario, senha)
            self._salvar_usuario()
            self.master.unbind_all('<Return>')
            self._abrir_dashboard(colaborador)

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            self.ent_senha.delete(0, tk.END)
            self.ent_senha.focus()
        except Exception as e:
            messagebox.showerror("Erro", "Falha interna no sistema")
            logging.error(f"Erro no login: {str(e)}")
        finally:
            if self.master.winfo_exists():
                self.btn_login.config(state=tk.NORMAL, text="Entrar")
                self.master.config(cursor="")

    def _abrir_dashboard(self, colaborador):
        from screens.home_view import HomeView

        # Reseta o cursor antes de destruir a janela
        self.master.config(cursor="")

        # Destroi a janela atual (login)
        self.master.destroy()

        # Cria nova janela principal como Toplevel
        root = tk.Tk()
        root.title("Controle de Atividades")

        try:
            root.iconbitmap("assets/icon.ico")
        except Exception as e:
            logging.warning(f"Erro ao definir ícone: {e}")

        HomeView(root, colaborador)
        root.mainloop()

