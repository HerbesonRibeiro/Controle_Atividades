# import tkinter as tk
# from tkinter import ttk
# from screens.registro_atividade_view import RegistroAtividadeView
# from screens.historico_atividades_view import HistoricoAtividadesView
# # from screens.perfil_view import PerfilView  # Se quiser implementar depois
#
# class HomeView:
#     def __init__(self, master, colaborador):
#         self.master = master
#         self.colaborador = colaborador
#         self.master.title("Controle de Atividades")
#         self.master.geometry("1000x650")
#         self.master.configure(bg="#f8f9fa")
#         self.master.resizable(True, True)
#
#         self._setup_ui()
#
#     def _setup_ui(self):
#         # Layout base
#         self.frame_menu = tk.Frame(self.master, bg="#343a40", width=240)
#         self.frame_menu.pack(side="left", fill="y")
#
#         self.frame_conteudo = tk.Frame(self.master, bg="#f8f9fa")
#         self.frame_conteudo.pack(side="right", fill="both", expand=True)
#
#         # Título do menu
#         tk.Label(self.frame_menu, text="Controle de Atividades",
#                  fg="#ffffff", bg="#343a40", font=("Segoe UI", 13, "bold"),
#                  anchor="w", padx=15).pack(fill="x", pady=(20, 10))
#
#         # Seções do menu
#         self._criar_secao_menu("ATIVIDADES", [
#             ("📋 Registro de Atividades", self._abrir_registro_atividades),
#             ("🕓 Histórico de Atividades", self._abrir_historico_atividades)
#         ])
#
#         self._criar_secao_menu("CONFIGURAÇÕES", [
#             ("👤 Meu Perfil", self._abrir_perfil),
#             ("🚪 Sair", self._logout)
#         ])
#
#         # Tela inicial
#         self._abrir_boas_vindas()
#
#     def _criar_secao_menu(self, titulo, botoes):
#         """Cria uma seção de menu com título e lista de botões"""
#         tk.Label(self.frame_menu, text=titulo, fg="#adb5bd", bg="#343a40",
#                  font=("Segoe UI", 10, "bold"), anchor="w", padx=15).pack(fill="x", pady=(15, 5))
#
#         for texto, comando in botoes:
#             btn = tk.Button(self.frame_menu, text=texto, font=("Segoe UI", 10),
#                             bg="#495057", fg="#ffffff", bd=0, relief="flat",
#                             anchor="w", padx=15,
#                             activebackground="#6c757d", command=comando)
#             btn.pack(fill="x", padx=10, pady=2)
#
#     def _limpar_conteudo(self):
#         for widget in self.frame_conteudo.winfo_children():
#             widget.destroy()
#
#     def _abrir_boas_vindas(self):
#         self._limpar_conteudo()
#         tk.Label(self.frame_conteudo,
#                  text=f"Bem-vindo, {self.colaborador.nome}",
#                  font=("Segoe UI", 18, "bold"),
#                  bg="#f8f9fa", fg="#343a40").pack(pady=60)
#
#     def _abrir_registro_atividades(self):
#         self._limpar_conteudo()
#         RegistroAtividadeView(self.frame_conteudo, self.colaborador)
#
#     def _abrir_historico_atividades(self):
#         self._limpar_conteudo()
#         HistoricoAtividadesView(self.frame_conteudo, self.colaborador)
#
#     def _abrir_perfil(self):
#         self._limpar_conteudo()
#         tk.Label(self.frame_conteudo,
#                  text="Em breve: Visualização do Perfil",
#                  font=("Segoe UI", 14),
#                  bg="#f8f9fa").pack(pady=50)
#
#     def _logout(self):
#         self.master.destroy()
#         from screens.login_view import LoginView
#         root = tk.Tk()
#         LoginView(root)
#         root.mainloop()

import tkinter as tk
from tkinter import ttk
from screens.registro_atividade_view import RegistroAtividadeView
from screens.historico_atividades_view import HistoricoAtividadesView
# from screens.perfil_view import PerfilView  # Se quiser implementar depois

class HomeView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.master.title("Controle de Atividades")
        self.master.geometry("1000x650")
        self.master.configure(bg="#f8f9fa")
        self.master.resizable(True, True)

        self._setup_ui()

    def _setup_ui(self):
        # Layout base
        self.frame_menu = tk.Frame(self.master, bg="#343a40", width=240)
        self.frame_menu.pack(side="left", fill="y")

        self.frame_conteudo = tk.Frame(self.master, bg="#f8f9fa")
        self.frame_conteudo.pack(side="right", fill="both", expand=True)

        # Espaço para LOGO
        tk.Frame(self.frame_menu, bg="#343a40", height=80).pack(fill="x")

        # Título do menu
        tk.Label(self.frame_menu, text="Controle de Atividades",
                 fg="#ffffff", bg="#343a40", font=("Segoe UI", 16, "bold"),
                 anchor="w", padx=15).pack(fill="x", pady=(20, 30))

        # Seções do menu
        self._criar_secao_menu("ATIVIDADES", [
            ("📋 Registro de Atividades", self._abrir_registro_atividades),
            ("🕓 Histórico de Atividades", self._abrir_historico_atividades)
        ])

        # Separador visual
        tk.Frame(self.frame_menu, bg="#343a40", height=2).pack(fill="x", pady=10)

        self._criar_secao_menu("CONFIGURAÇÕES", [
            ("👤 Meu Perfil", self._abrir_perfil),
            ("🚪 Sair", self._logout)
        ])

        # Tela inicial
        self._abrir_boas_vindas()

    def _criar_secao_menu(self, titulo, botoes):
        """Cria uma seção de menu com título e lista de botões"""
        tk.Label(self.frame_menu, text=titulo, fg="#adb5bd", bg="#343a40",
                 font=("Segoe UI", 10, "bold"), anchor="w", padx=15).pack(fill="x", pady=(10, 5))

        for texto, comando in botoes:
            btn = tk.Button(self.frame_menu, text=texto, font=("Segoe UI", 10),
                            bg="#495057", fg="#ffffff", bd=0, relief="flat",
                            anchor="w", padx=15,
                            activebackground="#6c757d", command=comando)
            btn.pack(fill="x", padx=10, pady=2)

    def _limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def _abrir_boas_vindas(self):
        self._limpar_conteudo()
        tk.Label(self.frame_conteudo,
                 text=f"Bem-vindo, {self.colaborador.nome}",
                 font=("Segoe UI", 18, "bold"),
                 bg="#f8f9fa", fg="#343a40",
                 anchor="center").pack(pady=(40, 20))

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
                 bg="#f8f9fa").pack(pady=50)

    def _logout(self):
        self.master.destroy()
        from screens.login_view import LoginView
        root = tk.Tk()
        LoginView(root)
        root.mainloop()