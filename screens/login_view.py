import tkinter as tk
from tkinter import ttk, messagebox
import logging
from controllers.auth_controller import AuthController


class LoginView:
    def __init__(self, master):
        self.master = master
        self.controller = AuthController()

        # Configurações da janela
        self.master.title("Controle de Atividades")
        self.master.geometry("380x320")
        self.master.resizable(False, False)
        self.master.configure(bg='#f8f9fa')
        self.master.eval('tk::PlaceWindow . center')

        self._setup_ui()

    def _setup_ui(self):
        """Configura todos os componentes da interface"""
        self.main_frame = tk.Frame(self.master, bg='#f8f9fa', padx=30, pady=20)
        self.main_frame.pack(expand=True, fill='both')

        # Título (ou logo)
        try:
            self.logo = tk.PhotoImage(file="assets/logo.vermelho.png").subsample(2, 2)
            tk.Label(self.main_frame, image=self.logo, bg='#f8f9fa').pack(pady=(0, 20))
        except:
            tk.Label(
                self.main_frame,
                text="Controle de Atividades",
                font=('Segoe UI', 16, 'bold'),
                bg='#f8f9fa',
                fg='#343a40'
            ).pack(pady=(0, 20))

        # Campo de usuário
        tk.Label(self.main_frame, text="Usuário", bg='#f8f9fa', fg='#495057', font=('Segoe UI', 10, 'bold')).pack(
            anchor='w')
        self.ent_usuario = tk.Entry(self.main_frame, font=('Segoe UI', 10), bd=1, relief='solid')
        self.ent_usuario.pack(fill='x', pady=(0, 15), ipady=5)
        self.ent_usuario.focus()

        # Campo de senha
        tk.Label(self.main_frame, text="Senha", bg='#f8f9fa', fg='#495057', font=('Segoe UI', 10, 'bold')).pack(
            anchor='w')

        senha_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        senha_frame.pack(fill='x')

        self.ent_senha = tk.Entry(senha_frame, font=('Segoe UI', 10), bd=1, relief='solid', show="•")
        self.ent_senha.pack(side='left', fill='x', expand=True, ipady=5)

        self.btn_show_pwd = tk.Button(
            senha_frame,
            text="👁",
            width=3,
            command=self._toggle_password,
            bg='#dee2e6',
            bd=0,
            relief='flat',
            activebackground='#ced4da'
        )
        self.btn_show_pwd.pack(side='right', padx=(5, 0))

        # Botão de login
        self.btn_login = tk.Button(
            self.main_frame,
            text="Entrar",
            command=self._on_login,
            bg='#4e73df',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            activebackground='#375aba',
            bd=0,
            height=2
        )
        self.btn_login.pack(fill='x', pady=(20, 10))

        # Link para esqueceu a senha
        tk.Label(
            self.main_frame,
            text="Esqueceu a senha?",
            fg="#6c757d",
            bg='#f8f9fa',
            font=('Segoe UI', 9, 'underline'),
            cursor="hand2"
        ).pack()

        # Tecla Enter faz login
        self.master.bind('<Return>', lambda e: self._on_login())

    def _toggle_password(self):
        if self.ent_senha.cget('show') == '•':
            self.ent_senha.config(show='')
            self.btn_show_pwd.config(text='🚫')
        else:
            self.ent_senha.config(show='•')
            self.btn_show_pwd.config(text='👁')

    def _on_login(self):
        """Handle do processo de login"""
        try:
            usuario = self.ent_usuario.get().strip()
            senha = self.ent_senha.get().strip()

            if not usuario or not senha:
                raise ValueError("Preencha todos os campos")

            # Feedback visual durante o login
            self.btn_login.config(state=tk.DISABLED, text="Autenticando...")
            self.master.config(cursor="wait")
            self.master.update()

            # Autenticação
            colaborador = self.controller.autenticar(usuario, senha)

            # Se autenticação for bem-sucedida
            self._abrir_dashboard(colaborador)

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            self.ent_senha.delete(0, tk.END)
            self.ent_senha.focus()
        except Exception as e:
            messagebox.showerror("Erro", "Falha interna no sistema")
            logging.error(f"Erro no login: {str(e)}")
        finally:
            self.btn_login.config(state=tk.NORMAL, text="Entrar")
            self.master.config(cursor="")

    def _abrir_dashboard(self, colaborador):
        """Fecha o login e abre a tela principal"""
        self.master.destroy()
        from screens.home_view import HomeView
        root = tk.Tk()
        HomeView(root, colaborador)
        root.mainloop()