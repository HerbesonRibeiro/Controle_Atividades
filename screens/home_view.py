# Revisado conexão com db
# import tkinter as tk
# from tkinter import ttk
# import sys
# import os
# from pathlib import Path
# from PIL import Image, ImageTk  # Requer pip install pillow
#
#
# class HomeView:
#     def __init__(self, master, colaborador):
#         # Verifica se já existe uma HomeView ativa - isso corrige abrir 2 janelas
#         for widget in master.winfo_children():
#             widget.destroy()
#
#         self.master = master
#         self.colaborador = colaborador
#         # ... resto do código ...
#         self.master = master
#         self.colaborador = colaborador
#         self.master.title("Controle de Atividades")
#         self.master.geometry("1000x650")
#         self.master.configure(bg="#f4f6f7")
#         self.master.resizable(True, True)
#
#         self._configurar_icone_janela()
#         self._configurar_estilos()
#         self._setup_ui()
#         self._centralizar_janela()
#
#     def _configurar_icone_janela(self):
#         try:
#             base_path = self._get_base_path()
#             icon_path = base_path / "assets" / "icon.ico"
#             if not icon_path.exists():
#                 raise FileNotFoundError(f"Arquivo de ícone não encontrado: {icon_path}")
#             if os.name == 'nt':
#                 self.master.iconbitmap(default=icon_path)
#
#             if hasattr(self.master, 'iconphoto'):
#                 img = Image.open(icon_path)
#                 photo = ImageTk.PhotoImage(img)
#                 self.master.iconphoto(True, photo)
#
#         except Exception as e:
#             print(f"Erro ao configurar ícone: {e}")
#
#     def _centralizar_janela(self):
#         """Centraliza a janela na tela do computador"""
#         self.master.update_idletasks()  # Atualiza as dimensões da janela
#         largura = self.master.winfo_width()
#         altura = self.master.winfo_height()
#         x = (self.master.winfo_screenwidth() // 2) - (largura // 2)
#         y = (self.master.winfo_screenheight() // 2) - (altura // 2)
#         self.master.geometry(f'+{x}+{y}')
#
#     def _configurar_estilos(self):
#         style = ttk.Style()
#         style.theme_use("clam")
#
#         style.configure("Sidebar.TFrame", background="#1f1f1f")
#         style.configure("MenuTitle.TLabel", background="#1f1f1f", foreground="#ffffff",
#                         font=("Segoe UI", 16, "bold"))
#         style.configure("MenuSection.TLabel", background="#1f1f1f", foreground="#e0e0e0",
#                         font=("Segoe UI", 10, "bold"))
#         style.configure("MenuButton.TButton", background="#2b2b2b", foreground="#ffffff",
#                         font=("Segoe UI", 10), borderwidth=0, anchor="w", padding=(10, 5))
#         style.map("MenuButton.TButton", background=[("active", "#3a3a3a")])
#         style.configure("Content.TFrame", background="#f4f6f7")
#         style.configure("Welcome.TLabel", background="#f4f6f7", foreground="#1f1f1f",
#                         font=("Segoe UI", 18, "bold"))
#         style.configure("Regular.TLabel", background="#f4f6f7", foreground="#1f1f1f",
#                         font=("Segoe UI", 14))
#
#     def _carregar_imagem(self, caminho_relativo, tamanho=None):
#         try:
#             base_path = self._get_base_path()
#             caminho_absoluto = base_path / caminho_relativo
#
#             if not caminho_absoluto.exists():
#                 raise FileNotFoundError(f"Arquivo não encontrado: {caminho_absoluto}")
#
#             imagem = Image.open(caminho_absoluto)
#             if tamanho:
#                 imagem = imagem.resize(tamanho, Image.LANCZOS)
#             return ImageTk.PhotoImage(imagem)
#
#         except Exception as e:
#             print(f"Erro ao carregar imagem: {e}")
#             return None
#
#     def _get_base_path(self):
#         if getattr(sys, 'frozen', False):
#             base_path = Path(sys._MEIPASS)
#         else:
#             base_path = Path(__file__).resolve().parent.parent
#         return base_path
#
#     def _setup_ui(self):
#         self.frame_menu = ttk.Frame(self.master, style="Sidebar.TFrame", width=240)
#         self.frame_menu.pack(side="left", fill="y")
#
#         self.frame_conteudo = ttk.Frame(self.master, style="Content.TFrame")
#         self.frame_conteudo.pack(side="right", fill="both", expand=True)
#
#         self.logo_img = self._carregar_imagem("assets/logo_vermelha.png", (120, 150))
#         if self.logo_img:
#             tk.Label(self.frame_menu, image=self.logo_img, bg="#1f1f1f").pack(pady=(25, 5))
#         else:
#             tk.Label(self.frame_menu, text="LOGO APP", bg="#1f1f1f",
#                      fg="white", font=("Arial", 14, "bold")).pack(pady=(25, 5))
#
#         ttk.Label(self.frame_menu, text="Controle de Atividades",
#                   style="MenuTitle.TLabel", anchor="w").pack(fill="x", padx=15, pady=(0, 20))
#
#         self._criar_secao_menu("ATIVIDADES", [
#             ("📋 Registro de Atividades", self._abrir_registro_atividades),
#             ("🕓 Histórico de Atividades", self._abrir_historico_atividades)
#         ])
#
#         ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=10, pady=12)
#
#         self._criar_secao_menu("CONFIGURAÇÕES", [
#             ("👤 Meu Perfil", self._abrir_perfil),
#             ("🚪 Sair", self._logout)
#         ])
#
#         ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=10, pady=12)
#
#         if self.colaborador.cargo.name == "ADMINISTRADOR":
#             self._criar_secao_menu("GESTÃO", [
#                 ("👤 Gerenciar Usuário", self._abrir_gerenciar_usuário),
#                 ("👨‍💼 Gerenciar Setores", self._abrir_gerenciar_setores),
#                 ("🧩 Gerenciar Tipos de Atividade", self._abrir_gerenciar_atividades),
#             ])
#
#         self._abrir_boas_vindas()
#
#     def _criar_secao_menu(self, titulo, botoes):
#         ttk.Label(self.frame_menu, text=titulo,
#                   style="MenuSection.TLabel", anchor="w").pack(fill="x", padx=15, pady=(10, 5))
#
#         for texto, comando in botoes:
#             ttk.Button(self.frame_menu, text=texto,
#                        style="MenuButton.TButton", command=comando).pack(fill="x", padx=15, pady=3)
#
#     def _limpar_conteudo(self):
#         for widget in self.frame_conteudo.winfo_children():
#             widget.destroy()
#
#     def _abrir_boas_vindas(self):
#         self._limpar_conteudo()
#         ttk.Label(self.frame_conteudo,
#                   text=f"Bem-vindo, {self.colaborador.nome}",
#                   style="Welcome.TLabel", anchor="center").pack(pady=(40, 20))
#
#     def _abrir_registro_atividades(self):
#         self._limpar_conteudo()
#         from screens.registro_atividade_view import RegistroAtividadeView
#         RegistroAtividadeView(self.frame_conteudo, self.colaborador)
#
#     def _abrir_historico_atividades(self):
#         self._limpar_conteudo()
#         from screens.historico_atividades_view import HistoricoAtividadesView
#         HistoricoAtividadesView(self.frame_conteudo, self.colaborador)
#
#     def _abrir_perfil(self):
#         self._limpar_conteudo()
#         from screens.perfil_view import PerfilView
#         PerfilView(self.frame_conteudo, self.colaborador)
#
#     def _abrir_gerenciar_usuário(self):
#         self._limpar_conteudo()
#         from screens.gerenciar_usuarios_view import GerenciarUsuariosView
#         GerenciarUsuariosView(self.frame_conteudo, self.colaborador)
#
#     def _abrir_gerenciar_setores(self):
#         self._limpar_conteudo()
#         from screens.cadastro_setor_view import CadastroSetorView
#         CadastroSetorView(self.frame_conteudo)
#
#     def _abrir_gerenciar_atividades(self):
#         self._limpar_conteudo()
#         from screens.cadastro_tipo_atividades import CadastroAtividadesView
#         CadastroAtividadesView(self.frame_conteudo)
#
#     def _logout(self):
#         self.frame_menu.destroy()
#         self.frame_conteudo.destroy()
#         from screens.login_view import LoginView
#         LoginView(self.master)

# Versão FINAL com correção de Janela (Centralizar e Maximizar)
import tkinter as tk
from tkinter import ttk
import sys
import os
from pathlib import Path
from PIL import Image, ImageTk
from pip._internal.utils import logging

from utils.db import Database


class HomeView:
    def __init__(self, master, colaborador):
        for widget in master.winfo_children():
            widget.destroy()

        self.master = master
        self.colaborador = colaborador
        self.active_button = None

        self.master.title("Controle de Atividades")

        # <<< CORREÇÃO: Lógica de inicialização da janela simplificada e corrigida >>>
        self.master.minsize(1100, 700)  # Define um tamanho mínimo para a janela
        self.master.resizable(True, True)  # Permite que a janela seja redimensionada e maximizada
        self.master.state('zoomed')  # Inicia a janela já maximizada

        self.master.configure(bg="#f4f6f7")

        self._configurar_icone_janela()
        self._configurar_estilos()
        self._setup_ui()
        # A chamada para _centralizar_janela() foi removida, pois 'zoomed' já cuida disso.

    def _configurar_icone_janela(self):
        try:
            icon_path = self._get_base_path() / "assets" / "icon.ico"
            if icon_path.exists(): self.master.iconbitmap(default=icon_path)
        except Exception as e:
            print(f"Erro ao configurar ícone: {e}")

    # <<< CORREÇÃO: Método _centralizar_janela() removido por não ser mais necessário >>>

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        BG_COLOR = "#f8f9fa";
        SIDEBAR_BG = "#212529";
        SIDEBAR_FG = "#e9ecef";
        PRIMARY_BLUE = "#007bff"
        style.configure(".", font=('Segoe UI', 10), background=BG_COLOR, foreground='#212529')
        style.configure("TFrame", background=BG_COLOR)
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
        style.map("Danger.TButton", background=[('active', '#c82333')])

    def _get_base_path(self):
        try:
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            base_path = Path(__file__).resolve().parent.parent
        return base_path

    def _carregar_imagem(self, caminho_relativo, tamanho=None):
        try:
            path = self._get_base_path() / caminho_relativo
            imagem = Image.open(path).resize(tamanho, Image.LANCZOS) if tamanho else Image.open(path)
            return ImageTk.PhotoImage(imagem)
        except Exception as e:
            print(f"Erro ao carregar imagem {caminho_relativo}: {e}"); return None

    def _setup_ui(self):
        self.frame_menu = ttk.Frame(self.master, style="Sidebar.TFrame", width=250)
        self.frame_menu.pack(side="left", fill="y");
        self.frame_menu.pack_propagate(False)
        self.frame_conteudo = ttk.Frame(self.master, style="TFrame")
        self.frame_conteudo.pack(side="right", fill="both", expand=True)
        self.logo_img = self._carregar_imagem("assets/logo_vermelha.png", (100, 120))
        if self.logo_img: ttk.Label(self.frame_menu, image=self.logo_img, style="Sidebar.TLabel").pack(pady=20)
        ttk.Label(self.frame_menu, text="Controle de Atividades", style="MenuTitle.TLabel").pack(pady=(0, 18), padx=15,
                                                                                                 anchor='w')
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
        ttk.Label(self.frame_conteudo, text="Tela de Perfil (Em Construção)", font=("Segoe UI", 18)).pack(expand=True)

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
        # <<< NOVO: Finalizando a sessão no banco de dados >>>
        try:
            if hasattr(self.colaborador, 'session_id') and self.colaborador.session_id:
                db = Database()  # Pega a instância do banco
                query = """
                    UPDATE log_acessos 
                    SET logout_timestamp = NOW(), status = 'INATIVO' 
                    WHERE id = %s
                """
                db.execute_query(query, (self.colaborador.session_id,), fetch=False)
        except Exception as e:
            logging.error(f"Falha ao finalizar log de acesso: {e}")

        self.frame_menu.destroy()
        self.frame_conteudo.destroy()
        from screens.login_view import LoginView
        LoginView(self.master)
