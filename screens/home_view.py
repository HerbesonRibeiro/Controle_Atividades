import tkinter as tk
from tkinter import ttk
from screens.registro_atividade_view import RegistroAtividadeView
from screens.historico_atividades_view import HistoricoAtividadesView
# from utils.auth_utils import logout_usuario  # Se quiser implementar depois

class HomeView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.master.title("Controle de Atividades")
        self.master.geometry("900x600")
        self.master.configure(bg="#f8f9fa")
        self.master.resizable(True, True)

        self._setup_ui()

    def _setup_ui(self):
        # Frame principal (2 colunas: menu lateral + conteúdo)
        self.frame_menu = tk.Frame(self.master, bg="#343a40", width=200)
        self.frame_menu.pack(side="left", fill="y")

        self.frame_conteudo = tk.Frame(self.master, bg="#ffffff")
        self.frame_conteudo.pack(side="right", fill="both", expand=True)

        # Botões de menu
        tk.Label(self.frame_menu, text="MENU", fg="#ffffff", bg="#343a40",
                 font=("Segoe UI", 12, "bold")).pack(pady=(20, 10))

        self._criar_botao_menu("Registro de Atividades", self._abrir_registro_atividades)
        self._criar_botao_menu("Histórico de Atividades", self._abrir_historico_atividades)
        self._criar_botao_menu("Meu Perfil", self._abrir_perfil)
        self._criar_botao_menu("Sair", self._logout)

        # Exibição inicial
        self._abrir_boas_vindas()

    def _criar_botao_menu(self, texto, comando):
        btn = tk.Button(self.frame_menu, text=texto, font=("Segoe UI", 10),
                        bg="#495057", fg="#ffffff", bd=0, relief="flat",
                        activebackground="#6c757d", command=comando)
        btn.pack(fill="x", pady=5, padx=10)

    def _limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def _abrir_boas_vindas(self):
        self._limpar_conteudo()
        tk.Label(self.frame_conteudo,
                 text=f"Bem-vindo, {self.colaborador.nome}",
                 font=("Segoe UI", 16),
                 bg="#ffffff", fg="#343a40").pack(pady=50)

    def _abrir_registro_atividades(self):
        self._limpar_conteudo()
        RegistroAtividadeView(self.frame_conteudo, self.colaborador)

    def _abrir_historico_atividades(self):
        self._limpar_conteudo()
        HistoricoAtividadesView(self.frame_conteudo, self.colaborador)

    def _abrir_perfil(self):
        self._limpar_conteudo()
        tk.Label(self.frame_conteudo,
                 text="Em breve: Visualização do Perfil",
                 font=("Segoe UI", 14),
                 bg="#ffffff").pack(pady=50)

    def _logout(self):
        self.master.destroy()
        from screens.login_view import LoginView
        root = tk.Tk()
        LoginView(root)
        root.mainloop()