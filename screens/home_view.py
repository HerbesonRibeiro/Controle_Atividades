import tkinter as tk
from tkinter import ttk

import self

from screens.registro_atividade_view import RegistroAtividadeView
from screens.historico_atividades_view import HistoricoAtividadesView
from screens.perfil_view import PerfilView

class HomeView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.master.title("Controle de Atividades")
        self.master.geometry("1000x650")
        self.master.configure(bg="#f8f9fa")
        self.master.resizable(True, True)

        self._configurar_estilos()
        self._setup_ui()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")  # mais moderno que 'default'

        style.configure("Sidebar.TFrame", background="#343a40")
        style.configure("MenuTitle.TLabel", background="#343a40", foreground="#ffffff",
                        font=("Segoe UI", 16, "bold"))

        style.configure("MenuSection.TLabel", background="#343a40", foreground="#adb5bd",
                        font=("Segoe UI", 10, "bold"))

        style.configure("MenuButton.TButton", background="#495057", foreground="#ffffff",
                        font=("Segoe UI", 10), borderwidth=0, anchor="w", padding=(10, 5))
        style.map("MenuButton.TButton", background=[("active", "#6c757d")])

        style.configure("Content.TFrame", background="#f8f9fa")
        style.configure("Welcome.TLabel", background="#f8f9fa", foreground="#343a40",
                        font=("Segoe UI", 18, "bold"))

        style.configure("Regular.TLabel", background="#f8f9fa", foreground="#343a40",
                        font=("Segoe UI", 14))

    def _setup_ui(self):
        # Lateral
        self.frame_menu = ttk.Frame(self.master, style="Sidebar.TFrame", width=240)
        self.frame_menu.pack(side="left", fill="y")

        # Conteúdo principal
        self.frame_conteudo = ttk.Frame(self.master, style="Content.TFrame")
        self.frame_conteudo.pack(side="right", fill="both", expand=True)

        try:
            self.logo_img = tk.PhotoImage(file="assets/logo_vermelha.png").subsample(3, 3)
            tk.Label(self.frame_menu, image=self.logo_img, bg="#343a40").pack(pady=(25, 5))
        except Exception:
            tk.Label(self.frame_menu, text="LOGO", bg="#343a40", fg="#ffffff").pack(pady=(25, 5))

        # Título do menu
        ttk.Label(self.frame_menu, text="Controle de Atividades",
                  style="MenuTitle.TLabel", anchor="w").pack(fill="x", padx=15, pady=(0, 20))

        # Seções do menu
        self._criar_secao_menu("ATIVIDADES", [
            ("📋 Registro de Atividades", self._abrir_registro_atividades),
            ("🕓 Histórico de Atividades", self._abrir_historico_atividades)
        ])

        # Separador
        ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=10, pady=12)

        self._criar_secao_menu("CONFIGURAÇÕES", [
            ("👤 Meu Perfil", self._abrir_perfil),
            ("🚪 Sair", self._logout)
        ])

        # Separador
        ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=10, pady=12)

        #Criar a seção do menu Gestão
        if self.colaborador.cargo.name == "ADMINISTRADOR":
            self._criar_secao_menu("GESTÃO", [
            ("👤 Gerenciar Usuário", self._abrir_gerenciar_usuário),
            ("👨‍💼 Gerenciar Setores", self._abrir_gerenciar_setores),
            ("🧩 Gerenciar Tipos de Atividade", self._abrir_gerenciar_atividades),
            ])

        # Tela inicial
        self._abrir_boas_vindas()
    def _criar_secao_menu(self, titulo, botoes):
        ttk.Label(self.frame_menu, text=titulo,
                  style="MenuSection.TLabel", anchor="w").pack(fill="x", padx=15, pady=(10, 5))

        for texto, comando in botoes:
            ttk.Button(self.frame_menu, text=texto,
                       style="MenuButton.TButton", command=comando).pack(fill="x", padx=15, pady=3)

    def _abrir_gerenciar_usuário(self):
        self._limpar_conteudo()
        from screens.gerenciar_usuarios_view import GerenciarUsuariosView
        GerenciarUsuariosView(self.frame_conteudo, self.colaborador)

    def _limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def _abrir_boas_vindas(self):
        self._limpar_conteudo()
        ttk.Label(self.frame_conteudo,
                  text=f"Bem-vindo, {self.colaborador.nome}",
                  style="Welcome.TLabel", anchor="center").pack(pady=(40, 20))

    def _abrir_registro_atividades(self):
        self._limpar_conteudo()
        RegistroAtividadeView(self.frame_conteudo, self.colaborador)

    def _abrir_historico_atividades(self):
        self._limpar_conteudo()
        HistoricoAtividadesView(self.frame_conteudo, self.colaborador)

    def _abrir_perfil(self):
        self._limpar_conteudo()
        from screens.perfil_view import PerfilView
        PerfilView(self.frame_conteudo, self.colaborador)

    def _abrir_gerenciar_setores(self):
        self._limpar_conteudo()
        from screens.cadastro_setor_view import CadastroSetorView
        CadastroSetorView(self.frame_conteudo)

    def _abrir_gerenciar_atividades(self):
        self._limpar_conteudo()
        from screens.cadastro_tipo_atividades import CadastroAtividadesView
        CadastroAtividadesView(self.frame_conteudo)

    def _logout(self):
        self.master.destroy()
        from screens.login_view import LoginView
        root = tk.Tk()
        LoginView(root)
        root.mainloop()