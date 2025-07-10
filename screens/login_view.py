import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController


class LoginView:
    def __init__(self, master):
        self.master = master # Janela principal
        self.controller = AuthController() #Instancia de controlador
        self._setup_ui() # Chama o método da construção de interface

        # Configuração inicial
        self.master.title("Controle de Atividades - Login")
        self.master.resizable(False, False) # Bloqueia redimencionamento
        self.master.eval('tk::PlaceWindow . center')  # Centraliza a janela

    def _setup_ui(self):
        """Configura todos os componentes da interface"""
        # Frame principal (container para organizar widgets)
        self.main_frame = ttk.Frame(self.master, padding=20)
        self.main_frame.pack()

        # Estilo
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10)) # Estilo para botões
        style.configure('TLabel', font=('Arial', 10)) # Estilo para labels

        # Campo de usuário
        ttk.Label(self.main_frame, text="Usuário:").grid(row=0, column=0, pady=5, sticky='w')
        self.ent_usuario = ttk.Entry(self.main_frame, width=25)
        self.ent_usuario.grid(row=0, column=1, pady=5)
        self.ent_usuario.focus()  # Foco inicial

        # Campo de senha
        ttk.Label(self.main_frame, text="Senha:").grid(row=1, column=0, pady=5, sticky='w')
        self.ent_senha = ttk.Entry(self.main_frame, show="•", width=25)
        self.ent_senha.grid(row=1, column=1, pady=5)

        # Botão de login
        self.btn_login = ttk.Button(
            self.main_frame,
            text="Entrar",
            command=self._on_login,
            style='TButton'
        )
        self.btn_login.grid(row=2, columnspan=2, pady=15)

        # Bind da tecla Enter
        self.ent_senha.bind('<Return>', lambda e: self._on_login())  # Aceita a tecla entre como botão entrar

    def _on_login(self):
        """Handle do processo de login"""
        usuario = self.ent_usuario.get().strip() # Remove espaços vazios de usuário
        senha = self.ent_senha.get().strip() # Remove espaços vazios de senha

        # Validação básica
        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            self.btn_login.config(state=tk.DISABLED, text="Autenticando...")
            self.master.update()  # Atualiza a interface

            # Autenticação real com controller
            usuario_autenticado = self.controller.autenticar(usuario, senha)
            self._abrir_dashboard(usuario_autenticado) # Login foi bem sucedido

        except ValueError as e:  # Erros de autenticação (Credenciais inválidas)
            messagebox.showerror("Erro", str(e))
            self.ent_senha.delete(0, tk.END)
            self.ent_senha.focus()
        except Exception as e:  # Outros erros
            messagebox.showerror("Erro", f"Falha no sistema: {str(e)}")
            # Log detalhado deveria ser feito aqui
        finally:
            self.btn_login.config(state=tk.NORMAL, text="Entrar")

    def _abrir_dashboard(self, usuario):
        """Fecha o login e abre a tela principal"""
        self.master.destroy()  # Fecha a janela de login
        from screens.home import HomeView  # Importação tardia para evitar circular
        root = tk.Tk()
        HomeView(root, usuario)
        root.mainloop()