# Arquivo: screens/home_view.py - VERSÃO FINAL
import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path
from PIL import Image, ImageTk
from utils.db import Database
from screens.perfil_view import PerfilView
import logging


class HomeView:
    def __init__(self, master, colaborador, on_logout):
        self.master = master
        self.colaborador = colaborador
        self.on_logout = on_logout
        self.active_button = None

        self.master.title("Controle de Atividades")
        self.master.minsize(1100, 700)
        self.master.resizable(True, True)
        self.master.state('zoomed')
        self.master.configure(bg="#f4f6f7")

        # <<< REMOVIDO: A chamada para configurar o ícone foi removida daqui >>>
        self._configurar_estilos()
        self._setup_ui()

    # <<< REMOVIDO: O método _configurar_icone_janela() foi removido daqui >>>

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        BG_COLOR = "#f8f9fa";
        SIDEBAR_BG = "#212529";
        SIDEBAR_FG = "#e9ecef";
        PRIMARY_BLUE = "#007bff"
        style.configure(".", font=('Segoe UI', 10), background=BG_COLOR, foreground='#212529')
        style.configure("TFrame", background=BG_COLOR)
        # ... (o resto do método de estilos continua igual) ...
        style.configure("TLabel", background=BG_COLOR)
        style.configure("TLabelframe", background=BG_COLOR, bordercolor="#dee2e6")
        style.configure("TLabelframe.Label", background=BG_COLOR, foreground="#495057", font=('Segoe UI', 10, 'bold'))
        style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
        style.configure("Sidebar.TLabel", background=SIDEBAR_BG, foreground=SIDEBAR_FG)
        style.configure("MenuTitle.TLabel", background=SIDEBAR_BG, foreground="#ffffff", font=("Segoe UI", 16, "bold"))
        style.configure("MenuSection.TLabel", background=SIDEBAR_BG, foreground="#adb5bd", font=("Segoe UI", 9, "bold"))
        style.configure("MenuButton.TButton", background="#343a40", foreground=SIDEBAR_FG, font=("Segoe UI", 10),
                        borderwidth=0, anchor="w", padding=(15, 10))
        style.map("MenuButton.TButton", background=[("active", "#495057")])
        style.configure("Selected.MenuButton.TButton", background=PRIMARY_BLUE, foreground="#ffffff")
        style.map("Selected.MenuButton.TButton", background=[("active", PRIMARY_BLUE)])
        style.configure("TButton", font=('Segoe UI', 9, 'bold'), padding=(8, 5), relief='flat', borderwidth=0)
        style.configure("Primary.TButton", background=PRIMARY_BLUE, foreground="white")
        style.map("Primary.TButton", background=[('active', '#0056b3')])
        style.configure("Danger.TButton", background="#dc3545", foreground="white")
        style.map("Danger.TButton", background=[("active", '#c82333')])

    def _get_base_path(self):  # <<< REMOVIDO: Lógica movida para o main.py >>>
        try:
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            base_path = Path(__file__).resolve().parent.parent
        return base_path

    # ... (o resto do arquivo continua exatamente o mesmo) ...
    def _carregar_imagem(self, caminho_relativo, tamanho=None):
        try:
            path = self._get_base_path() / caminho_relativo
            imagem = Image.open(path).resize(tamanho, Image.LANCZOS) if tamanho else Image.open(path)
            return ImageTk.PhotoImage(imagem)
        except Exception as e:
            print(f"Erro ao carregar imagem {caminho_relativo}: {e}");
            return None

    def _setup_ui(self):
        self.frame_menu = ttk.Frame(self.master, style="Sidebar.TFrame", width=280)
        self.frame_menu.pack(side="left", fill="y");
        self.frame_menu.pack_propagate(False)
        self.frame_conteudo = ttk.Frame(self.master, style="TFrame")
        self.frame_conteudo.pack(side="right", fill="both", expand=True)
        self.logo_img = self._carregar_imagem("assets/logo_vermelha.png", (100, 120))
        if self.logo_img: ttk.Label(self.frame_menu, image=self.logo_img, style="Sidebar.TLabel").pack(pady=20)

        title_label = ttk.Label(self.frame_menu, text="Controle de Atividades", style="MenuTitle.TLabel",
                                wraplength=250)
        title_label.pack(pady=(0, 18), padx=15, anchor='w')

        self._criar_secao_menu("ATIVIDADES", [("📋  Registro de Atividades", self._abrir_registro_atividades),
                                              ("🕓  Histórico de Atividades", self._abrir_historico_atividades)])
        ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=15, pady=15)
        self._criar_secao_menu("CONFIGURAÇÕES", [("👤  Meu Perfil", self._abrir_perfil), ("🚪  Sair", self._logout)])
        if self.colaborador.cargo.name == "ADMINISTRADOR":
            ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=15, pady=15)
            self._criar_secao_menu("GESTÃO", [("⚙️  Gerenciar Usuários", self._abrir_gerenciar_usuário),
                                              ("🏢  Gerenciar Setores", self._abrir_gerenciar_setores),
                                              ("📝  Gerenciar Tipos", self._abrir_gerenciar_atividades)])
        self._abrir_boas_vindas()

    def _criar_secao_menu(self, titulo, botoes):
        ttk.Label(self.frame_menu, text=titulo.upper(), style="MenuSection.TLabel").pack(fill="x", padx=15,
                                                                                         pady=(10, 5), anchor='w')
        for texto, comando in botoes:
            btn = ttk.Button(self.frame_menu, text=texto, style="MenuButton.TButton")
            btn.configure(command=self._criar_comando_menu(btn, comando))
            btn.pack(fill="x", padx=15, pady=2)

    def _criar_comando_menu(self, button, command):
        def on_click(): self._set_botao_ativo(button); command()

        return on_click

    def _set_botao_ativo(self, button):
        if self.active_button: self.active_button.configure(style="MenuButton.TButton")
        button.configure(style="Selected.MenuButton.TButton")
        self.active_button = button

    def _limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children(): widget.destroy()

    def _abrir_boas_vindas(self):
        self._limpar_conteudo()
        if self.active_button: self.active_button.configure(style="MenuButton.TButton"); self.active_button = None
        container = ttk.Frame(self.frame_conteudo)
        container.pack(expand=True)
        ttk.Label(container, text=f"Bem-vindo, {self.colaborador.nome}!", font=("Segoe UI", 22, "bold")).pack()
        ttk.Label(container, text="Selecione uma opção no menu à esquerda para começar.", font=("Segoe UI", 12)).pack()

    def _abrir_registro_atividades(self):
        self._limpar_conteudo()
        from screens.registro_atividade_view import RegistroAtividadeView
        RegistroAtividadeView(self.frame_conteudo, self.colaborador)

    def _abrir_historico_atividades(self):
        self._limpar_conteudo()
        from screens.historico_atividades_view import HistoricoAtividadesView
        HistoricoAtividadesView(self.frame_conteudo, self.colaborador)

    def _abrir_perfil(self):
        self._limpar_conteudo()
        PerfilView(self.frame_conteudo, self.colaborador)

    def _abrir_gerenciar_usuário(self):
        self._limpar_conteudo()
        from screens.gerenciar_usuarios_view import GerenciarUsuariosView
        GerenciarUsuariosView(self.frame_conteudo, self.colaborador)

    def _abrir_gerenciar_setores(self):
        self._limpar_conteudo()
        from screens.cadastro_setor_view import CadastroSetorView
        CadastroSetorView(self.frame_conteudo)

    def _abrir_gerenciar_atividades(self):
        self._limpar_conteudo()
        from screens.cadastro_tipo_atividades import CadastroAtividadesView
        CadastroAtividadesView(self.frame_conteudo)

    def _logout(self):
        try:
            if hasattr(self.colaborador, 'session_id') and self.colaborador.session_id:
                db = Database()
                query = "UPDATE log_acessos SET logout_timestamp = NOW(), status = 'INATIVO' WHERE id = %s"
                db.execute_query(query, (self.colaborador.session_id,), fetch=False)
        except Exception as e:
            logging.error(f"Falha ao finalizar log de acesso: {e}")

        self.on_logout()