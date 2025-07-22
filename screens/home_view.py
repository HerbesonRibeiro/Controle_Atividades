import tkinter as tk
from tkinter import ttk
import sys
import os
from pathlib import Path
from PIL import Image, ImageTk  # Requer pip install pillow


class HomeView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.master.title("Controle de Atividades")
        self.master.geometry("1000x650")
        self.master.configure(bg="#f8f9fa")
        self.master.resizable(True, True)

        # Esta linha para configurar o ícone
        self._configurar_icone_janela()


        self._configurar_estilos()
        self._setup_ui()

    def _configurar_icone_janela(self):
        """Configura o ícone da janela e barra de tarefas"""
        try:
            base_path = self._get_base_path()
            icon_path = base_path / "assets" / "icon.ico"  # Substitua pelo nome do seu arquivo de ícone


            if not icon_path.exists():
                raise FileNotFoundError(f"Arquivo de ícone não encontrado: {icon_path}")

            # Configura o ícone para Windows
            if os.name == 'nt':
                self.master.iconbitmap(default=icon_path)

            # Configuração adicional para garantir que apareça na barra de tarefas
            self.master.wm_iconbitmap()
            if hasattr(self.master, 'iconphoto'):
                img = Image.open(icon_path)
                photo = ImageTk.PhotoImage(img)
                self.master.iconphoto(True, photo)

        except Exception as e:
            print(f"Erro ao configurar ícone: {e}")
            # Continua sem ícone mas não quebra a aplicação


    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

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

    def _carregar_imagem(self, caminho_relativo, tamanho=None):
        """Método robusto para carregar imagens"""
        try:
            base_path = self._get_base_path()
            caminho_absoluto = base_path / caminho_relativo

            if not caminho_absoluto.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_absoluto}")

            imagem = Image.open(caminho_absoluto)
            if tamanho:
                imagem = imagem.resize(tamanho, Image.LANCZOS)
            return ImageTk.PhotoImage(imagem)

        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            return None

    def _get_base_path(self):
        """Determina o caminho base correto para recursos"""
        if getattr(sys, 'frozen', False):
            # Executável empacotado
            base_path = Path(sys._MEIPASS)
        else:
            # Modo desenvolvimento
            base_path = Path(__file__).resolve().parent.parent

        return base_path

    def _setup_ui(self):
        # Frame lateral (menu)
        self.frame_menu = ttk.Frame(self.master, style="Sidebar.TFrame", width=240)
        self.frame_menu.pack(side="left", fill="y")

        # Frame conteúdo principal
        self.frame_conteudo = ttk.Frame(self.master, style="Content.TFrame")
        self.frame_conteudo.pack(side="right", fill="both", expand=True)

        # Logo
        self.logo_img = self._carregar_imagem("assets/logo_vermelha.png", (120, 150))
        if self.logo_img:
            tk.Label(self.frame_menu, image=self.logo_img, bg="#343a40").pack(pady=(25, 5))
        else:
            tk.Label(self.frame_menu, text="LOGO APP", bg="#343a40",
                     fg="white", font=("Arial", 14, "bold")).pack(pady=(25, 5))

        # Título do menu
        ttk.Label(self.frame_menu, text="Controle de Atividades",
                  style="MenuTitle.TLabel", anchor="w").pack(fill="x", padx=15, pady=(0, 20))

        # Seções do menu
        self._criar_secao_menu("ATIVIDADES", [
            ("📋 Registro de Atividades", self._abrir_registro_atividades),
            ("🕓 Histórico de Atividades", self._abrir_historico_atividades)
        ])

        ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=10, pady=12)

        self._criar_secao_menu("CONFIGURAÇÕES", [
            ("👤 Meu Perfil", self._abrir_perfil),
            ("🚪 Sair", self._logout)
        ])

        ttk.Separator(self.frame_menu, orient="horizontal").pack(fill="x", padx=10, pady=12)

        if self.colaborador.cargo.name == "ADMINISTRADOR":
            self._criar_secao_menu("GESTÃO", [
                ("👤 Gerenciar Usuário", self._abrir_gerenciar_usuário),
                ("👨‍💼 Gerenciar Setores", self._abrir_gerenciar_setores),
                ("🧩 Gerenciar Tipos de Atividade", self._abrir_gerenciar_atividades),
            ])

        self._abrir_boas_vindas()

    def _criar_secao_menu(self, titulo, botoes):
        ttk.Label(self.frame_menu, text=titulo,
                  style="MenuSection.TLabel", anchor="w").pack(fill="x", padx=15, pady=(10, 5))

        for texto, comando in botoes:
            ttk.Button(self.frame_menu, text=texto,
                       style="MenuButton.TButton", command=comando).pack(fill="x", padx=15, pady=3)

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
        from screens.registro_atividade_view import RegistroAtividadeView
        RegistroAtividadeView(self.frame_conteudo, self.colaborador)

    def _abrir_historico_atividades(self):
        self._limpar_conteudo()
        from screens.historico_atividades_view import HistoricoAtividadesView
        HistoricoAtividadesView(self.frame_conteudo, self.colaborador)

    def _abrir_perfil(self):
        self._limpar_conteudo()
        from screens.perfil_view import PerfilView
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
        self.master.destroy()
        from screens.login_view import LoginView
        root = tk.Tk()
        LoginView(root)
        root.mainloop()