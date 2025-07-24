# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime
# from tkcalendar import Calendar
#
#
# class RegistroFlutuante:
#     def __init__(self, master, colaborador, dados_iniciais=None):
#         """Inicializa a janela flutuante de forma confiável"""
#         try:
#             # Cria a janela Toplevel
#             self.root = tk.Toplevel(master)
#             self.root.title("Registro Flutuante")
#
#             # Configurações essenciais
#             self.root.transient(master)  # Torna dependente da principal
#             self.root.grab_set()  # Modal
#
#             # Centraliza a janela
#             self._centralizar_janela()
#
#             # Variáveis e inicialização
#             self.colaborador = colaborador
#             self.var_tipo = tk.StringVar()
#             self.var_nivel = tk.StringVar()
#             self.var_status = tk.StringVar()
#             self._configurar_estilos()
#             self._setup_ui()
#
#             # Preenche os dados iniciais se fornecidos
#             if dados_iniciais:
#                 self._preencher_campos(dados_iniciais)
#
#             # Garante que a janela será exibida
#             self.root.after(100, self._verificar_visibilidade)
#
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             raise RuntimeError(f"Falha ao inicializar janela flutuante: {str(e)}")
#
#     def _verificar_visibilidade(self):
#         """Garante que a janela ficou visível"""
#         if not self.root.winfo_viewable():
#             self.root.deiconify()
#             self.root.lift()
#             self.root.after(100, self._verificar_visibilidade)
#
#     def _centralizar_janela(self):
#         """Centraliza a janela na tela"""
#         self.root.update_idletasks()
#         width = self.root.winfo_width()
#         height = self.root.winfo_height()
#         x = (self.root.winfo_screenwidth() // 2) - (width // 2)
#         y = (self.root.winfo_screenheight() // 2) - (height // 2)
#         self.root.geometry(f'+{x}+{y}')
#
#     def _configurar_estilos(self):
#         """Configura os estilos visuais"""
#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("TFrame", background="#f8f9fa")
#         style.configure("TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 10))
#         style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 18, "bold"))
#         style.configure("TEntry", font=("Segoe UI", 10))
#         style.configure("TButton", font=("Segoe UI", 10, "bold"))
#         style.configure("Primary.TButton", background="#4a6da7", foreground="white",
#                         font=("Segoe UI", 10, "bold"), padding=6)
#         style.configure("Flutuante.TButton", background="#6c757d", foreground="white",
#                         font=("Segoe UI", 10, "bold"), padding=6)
#         style.configure("Calendar.TButton", background="#4a6da7", foreground="white",
#                         font=("Segoe UI", 10, "bold"), padding=6)
#
#     def _carregar_tipos_atendimento(self):
#         """Carrega os tipos de atendimento (simplificado)"""
#         self.todos_tipos = {
#             "Consulta Médica": 1,
#             "Exame Laboratorial": 2,
#             "Atendimento Emergencial": 3
#         }
#         if hasattr(self, 'combo_tipo'):
#             self.combo_tipo['values'] = list(self.todos_tipos.keys())
#
#     def _setup_ui(self):
#         """Configura a interface do usuário"""
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.grid(row=0, column=0, sticky="nsew")
#         self._criar_campos(main_frame)
#         self._carregar_tipos_atendimento()
#
#     def _criar_campos(self, parent):
#         """Cria todos os campos do formulário"""
#         # Status
#         status_frame = ttk.Frame(parent)
#         status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
#
#         self.status_indicator = tk.Canvas(status_frame, width=16, height=16,
#                                          bg="#f8f9fa", highlightthickness=0)
#         self.status_indicator.pack(side="left", padx=(0, 5))
#         self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="gray")
#         ttk.Label(status_frame, text="Preencha os campos obrigatórios").pack(side="left")
#
#         # Campos do formulário
#         campos = [
#             ("Data de Atendimento:", "entry_data", datetime.today().strftime("%d/%m/%Y")),
#             ("Tipo de Atendimento:", "combo_tipo", []),
#             ("Nível de Complexidade:", "combo_nivel", ["baixo", "medio", "grave", "gravissimo"]),
#             ("Número/Ticket:", "entry_ticket", ""),
#             ("Status:", "combo_status", ["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"]),
#             ("Descrição:", "txt_descricao", "")
#         ]
#
#         for row, (label, var_name, default) in enumerate(campos, start=2):
#             ttk.Label(parent, text=label).grid(row=row, column=0, sticky="e", pady=4, padx=5)
#
#             if var_name == "combo_tipo":
#                 self.combo_tipo = ttk.Combobox(
#                     parent,
#                     textvariable=self.var_tipo,
#                     state="normal",
#                     width=40,
#                     font=("Segoe UI", 10)
#                 )
#                 self.combo_tipo.grid(row=row, column=1, pady=4, sticky="we", padx=5)
#                 self.combo_tipo.set("Digite para buscar...")
#
#             elif var_name == "combo_nivel":
#                 self.combo_nivel = ttk.Combobox(parent, textvariable=self.var_nivel,
#                                                 values=default, state="readonly")
#                 self.combo_nivel.grid(row=row, column=1, pady=4, sticky="we")
#                 self.combo_nivel.current(0)
#
#             elif var_name == "entry_data":
#                 frame = ttk.Frame(parent)
#                 frame.grid(row=row, column=1, sticky="we")
#                 self.entry_data = ttk.Entry(frame, width=15)
#                 self.entry_data.insert(0, default)
#                 self.entry_data.pack(side="left")
#                 ttk.Button(frame, text="🗓️ Escolher", command=self._abrir_calendario,
#                            style="Calendar.TButton").pack(side="left", padx=8)
#
#             elif var_name == "entry_ticket":
#                 self.entry_ticket = ttk.Entry(parent)
#                 self.entry_ticket.grid(row=row, column=1, sticky="we")
#
#             elif var_name == "txt_descricao":
#                 self.txt_descricao = tk.Text(parent, height=4, width=40, wrap="word")
#                 self.txt_descricao.grid(row=row, column=1, pady=4, sticky="we")
#
#             elif var_name == "combo_status":
#                 self.combo_status = ttk.Combobox(
#                     parent,
#                     textvariable=self.var_status,
#                     values=default,
#                     state="readonly"
#                 )
#                 self.combo_status.grid(row=row, column=1, pady=4, sticky="we")
#
#         # Botão de salvar
#         btn_salvar = ttk.Button(
#             parent,
#             text="Salvar (Ctrl+Enter)",
#             command=self._salvar,
#             style="Primary.TButton"
#         )
#         btn_salvar.grid(row=len(campos) + 2, column=1, pady=10, sticky="e")
#
#     def _abrir_calendario(self):
#         """Abre o calendário para seleção de data"""
#         top = tk.Toplevel(self.root)
#         top.title("Selecione a Data")
#
#         cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy")
#         cal.pack(pady=10)
#
#         ttk.Button(top, text="Selecionar", command=lambda: self._selecionar_data(cal, top),
#                    style="Primary.TButton").pack(pady=5)
#
#     def _selecionar_data(self, cal, top):
#         """Processa a data selecionada no calendário"""
#         self.entry_data.delete(0, tk.END)
#         self.entry_data.insert(0, cal.get_date())
#         top.destroy()
#
#     def _preencher_campos(self, dados):
#         """Preenche todos os campos com os dados iniciais"""
#         self.entry_data.delete(0, tk.END)
#         self.entry_data.insert(0, dados.get('data', ''))
#
#         self.combo_tipo.set(dados.get('tipo', ''))
#         self.combo_nivel.set(dados.get('nivel', 'baixo'))
#
#         self.entry_ticket.delete(0, tk.END)
#         self.entry_ticket.insert(0, dados.get('ticket', ''))
#
#         self.txt_descricao.delete("1.0", tk.END)
#         self.txt_descricao.insert("1.0", dados.get('descricao', '').strip())
#
#         if 'status' in dados and dados['status'] is not None:
#             self.combo_status.set(dados['status'])
#
#     def _salvar(self):
#         """Método para salvar os dados"""
#         messagebox.showinfo("Sucesso", "Dados salvos com sucesso!", parent=self.root)
#
#     def _fechar_janela(self):
#         """Fecha a janela flutuante"""
#         self.root.destroy()

# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime
# from tkcalendar import Calendar
#
#
# class RegistroFlutuante:
#     def __init__(self, master, colaborador, dados_iniciais=None):
#         """Inicializa a janela flutuante de forma confiável"""
#         try:
#             # Cria a janela Toplevel
#             self.root = tk.Toplevel(master)
#             self.root.title("Registro Flutuante")
#             self.root.minsize(500, 400)  # Tamanho mínimo para melhor apresentação
#
#             # Configurações essenciais
#             self.root.transient(master)  # Torna dependente da principal
#             self.root.grab_set()  # Modal
#
#             # Centraliza a janela
#             self._centralizar_janela()
#
#             # Variáveis e inicialização
#             self.colaborador = colaborador
#             self.var_tipo = tk.StringVar()
#             self.var_nivel = tk.StringVar()
#             self.var_status = tk.StringVar()
#             self._configurar_estilos()
#             self._setup_ui()
#
#             # Preenche os dados iniciais se fornecidos
#             if dados_iniciais:
#                 self._preencher_campos(dados_iniciais)
#
#             # Garante que a janela será exibida
#             self.root.after(100, self._verificar_visibilidade)
#
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             raise RuntimeError(f"Falha ao inicializar janela flutuante: {str(e)}")
#
#     def _verificar_visibilidade(self):
#         """Garante que a janela ficou visível"""
#         if not self.root.winfo_viewable():
#             self.root.deiconify()
#             self.root.lift()
#             self.root.after(100, self._verificar_visibilidade)
#
#     def _centralizar_janela(self):
#         """Centraliza a janela na tela"""
#         self.root.update_idletasks()
#         width = max(self.root.winfo_width(), 500)  # Usa tamanho mínimo
#         height = max(self.root.winfo_height(), 400)
#         x = (self.root.winfo_screenwidth() // 2) - (width // 2)
#         y = (self.root.winfo_screenheight() // 2) - (height // 2)
#         self.root.geometry(f'{width}x{height}+{x}+{y}')
#
#     def _configurar_estilos(self):
#         """Configura os estilos visuais"""
#         style = ttk.Style()
#         style.theme_use("clam")
#
#         # Configurações gerais
#         style.configure("TFrame", background="#e9ecef")  # Fundo cinza claro
#         style.configure("TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 11))
#         style.configure("Title.TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 16, "bold"))
#         style.configure("TEntry", font=("Roboto", 11), padding=5)
#         style.configure("TCombobox", font=("Roboto", 11), padding=5)
#         style.configure("TButton", font=("Roboto", 11, "bold"), padding=8)
#
#         # Estilo para botões principais
#         style.configure("Primary.TButton", background="#007bff", foreground="white",
#                         bordercolor="#0056b3", lightcolor="#007bff", darkcolor="#0056b3")
#         style.map("Primary.TButton",
#                   background=[('active', '#0056b3'), ('!disabled', '#007bff')],
#                   foreground=[('active', 'white'), ('!disabled', 'white')])
#
#         # Estilo para botão de fechar
#         style.configure("Cancel.TButton", background="#6c757d", foreground="white",
#                         bordercolor="#5a6268", lightcolor="#6c757d", darkcolor="#5a6268")
#         style.map("Cancel.TButton",
#                   background=[('active', '#5a6268'), ('!disabled', '#6c757d')],
#                   foreground=[('active', 'white'), ('!disabled', 'white')])
#
#         # Estilo para botão do calendário
#         style.configure("Calendar.TButton", background="#17a2b8", foreground="white",
#                         bordercolor="#117a8b", lightcolor="#17a2b8", darkcolor="#117a8b")
#         style.map("Calendar.TButton",
#                   background=[('active', '#117a8b'), ('!disabled', '#17a2b8')],
#                   foreground=[('active', 'white'), ('!disabled', 'white')])
#
#     def _carregar_tipos_atendimento(self):
#         """Carrega os tipos de atendimento (simplificado)"""
#         self.todos_tipos = {
#             "Consulta Médica": 1,
#             "Exame Laboratorial": 2,
#             "Atendimento Emergencial": 3
#         }
#         if hasattr(self, 'combo_tipo'):
#             self.combo_tipo['values'] = list(self.todos_tipos.keys())
#
#     def _setup_ui(self):
#         """Configura a interface do usuário"""
#         main_frame = ttk.Frame(self.root, padding="20")  # Maior padding
#         main_frame.grid(row=0, column=0, sticky="nsew")
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         self._criar_campos(main_frame)
#         self._carregar_tipos_atendimento()
#
#     def _criar_campos(self, parent):
#         """Cria todos os campos do formulário"""
#         # Título
#         ttk.Label(parent, text="Novo Registro", style="Title.TLabel").grid(
#             row=0, column=0, columnspan=2, pady=(0, 15), sticky="w"
#         )
#
#         # Status
#         status_frame = ttk.Frame(parent)
#         status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))
#         self.status_indicator = tk.Canvas(status_frame, width=20, height=20,
#                                          bg="#e9ecef", highlightthickness=0)
#         self.status_indicator.pack(side="left", padx=(0, 8))
#         self.status_circle = self.status_indicator.create_oval(4, 4, 16, 16, fill="#6c757d")
#         ttk.Label(status_frame, text="Preencha os campos obrigatórios").pack(side="left")
#
#         # Campos do formulário
#         campos = [
#             ("Data de Atendimento:", "entry_data", datetime.today().strftime("%d/%m/%Y")),
#             ("Tipo de Atendimento:", "combo_tipo", []),
#             ("Nível de Complexidade:", "combo_nivel", ["baixo", "médio", "grave", "gravíssimo"]),
#             ("Número/Ticket:", "entry_ticket", ""),
#             ("Status:", "combo_status", ["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"]),
#             ("Descrição:", "txt_descricao", "")
#         ]
#
#         for row, (label, var_name, default) in enumerate(campos, start=2):
#             ttk.Label(parent, text=label).grid(row=row, column=0, sticky="e", pady=6, padx=10)
#
#             if var_name == "combo_tipo":
#                 self.combo_tipo = ttk.Combobox(
#                     parent,
#                     textvariable=self.var_tipo,
#                     state="normal",
#                     width=50,  # Aumentado para melhor visual
#                     font=("Roboto", 11)
#                 )
#                 self.combo_tipo.grid(row=row, column=1, pady=6, sticky="we", padx=10)
#                 self.combo_tipo.set("Digite para buscar...")
#
#             elif var_name == "combo_nivel":
#                 self.combo_nivel = ttk.Combobox(parent, textvariable=self.var_nivel,
#                                                 values=default, state="readonly", width=50)
#                 self.combo_nivel.grid(row=row, column=1, pady=6, sticky="we", padx=10)
#                 self.combo_nivel.current(0)
#
#             elif var_name == "entry_data":
#                 frame = ttk.Frame(parent)
#                 frame.grid(row=row, column=1, sticky="we", padx=10)
#                 self.entry_data = ttk.Entry(frame, width=20, font=("Roboto", 11))
#                 self.entry_data.insert(0, default)
#                 self.entry_data.pack(side="left")
#                 ttk.Button(frame, text="🗓️", command=self._abrir_calendario,
#                            style="Calendar.TButton", width=4).pack(side="left", padx=10)
#
#             elif var_name == "entry_ticket":
#                 self.entry_ticket = ttk.Entry(parent, width=50, font=("Roboto", 11))
#                 self.entry_ticket.grid(row=row, column=1, sticky="we", padx=10)
#
#             elif var_name == "txt_descricao":
#                 self.txt_descricao = tk.Text(parent, height=5, width=50, wrap="word",
#                                              font=("Roboto", 11))
#                 self.txt_descricao.grid(row=row, column=1, pady=6, sticky="we", padx=10)
#
#             elif var_name == "combo_status":
#                 self.combo_status = ttk.Combobox(
#                     parent,
#                     textvariable=self.var_status,
#                     values=default,
#                     state="readonly",
#                     width=50,
#                     font=("Roboto", 11)
#                 )
#                 self.combo_status.grid(row=row, column=1, pady=6, sticky="we", padx=10)
#
#         # Frame para botões
#         button_frame = ttk.Frame(parent)
#         button_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=20, sticky="e")
#         ttk.Button(
#             button_frame,
#             text="Salvar (Ctrl+Enter)",
#             command=self._salvar,
#             style="Primary.TButton"
#         ).pack(side="right", padx=5)
#         ttk.Button(
#             button_frame,
#             text="Fechar",
#             command=self._fechar_janela,
#             style="Cancel.TButton"
#         ).pack(side="right", padx=5)
#
#     def _abrir_calendario(self):
#         """Abre o calendário para seleção de data"""
#         top = tk.Toplevel(self.root)
#         top.title("Selecione a Data")
#         top.transient(self.root)
#         top.grab_set()
#         top.minsize(300, 300)
#
#         cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy", font=("Roboto", 10))
#         cal.pack(pady=20, padx=20)
#
#         ttk.Button(top, text="Selecionar", command=lambda: self._selecionar_data(cal, top),
#                    style="Primary.TButton").pack(pady=10)
#
#     def _selecionar_data(self, cal, top):
#         """Processa a data selecionada no calendário"""
#         self.entry_data.delete(0, tk.END)
#         self.entry_data.insert(0, cal.get_date())
#         top.destroy()
#
#     def _preencher_campos(self, dados):
#         """Preenche todos os campos com os dados iniciais"""
#         self.entry_data.delete(0, tk.END)
#         self.entry_data.insert(0, dados.get('data', ''))
#
#         self.combo_tipo.set(dados.get('tipo', ''))
#         self.combo_nivel.set(dados.get('nivel', 'baixo'))
#
#         self.entry_ticket.delete(0, tk.END)
#         self.entry_ticket.insert(0, dados.get('ticket', ''))
#
#         self.txt_descricao.delete("1.0", tk.END)
#         self.txt_descricao.insert("1.0", dados.get('descricao', '').strip())
#
#         if 'status' in dados and dados['status'] is not None:
#             self.combo_status.set(dados['status'])
#
#     def _salvar(self):
#         """Método para salvar os dados"""
#         messagebox.showinfo("Sucesso", "Dados salvos com sucesso!", parent=self.root)
#
#     def _fechar_janela(self):
#         """Fecha a janela flutuante"""
#         self.root.destroy()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar


class RegistroFlutuante:
    def __init__(self, master, colaborador, dados_iniciais=None):
        """Inicializa a janela flutuante de forma confiável"""
        try:
            # Cria a janela Toplevel
            self.root = tk.Toplevel(master)
            self.root.title("Registro Flutuante")
            self.root.minsize(400, 300)  # Tamanho inicial compacto

            # Configurações essenciais
            self.root.transient(master)  # Torna dependente da principal
            self.root.grab_set()  # Modal

            # Centraliza a janela
            self._centralizar_janela()

            # Variáveis e inicialização
            self.colaborador = colaborador
            self.var_tipo = tk.StringVar()
            self.var_nivel = tk.StringVar()
            self.var_status = tk.StringVar()
            self._configurar_estilos()
            self._setup_ui()

            # Preenche os dados iniciais se fornecidos
            if dados_iniciais:
                self._preencher_campos(dados_iniciais)

            # Garante que a janela será exibida
            self.root.after(100, self._verificar_visibilidade)

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Falha ao inicializar janela flutuante: {str(e)}")

    def _verificar_visibilidade(self):
        """Garante que a janela ficou visível"""
        if not self.root.winfo_viewable():
            self.root.deiconify()
            self.root.lift()
            self.root.after(100, self._verificar_visibilidade)

    def _centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 500  # Tamanho fixo inicial
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _configurar_estilos(self):
        """Configura os estilos visuais"""
        style = ttk.Style()
        style.theme_use("clam")

        # Configurações gerais
        style.configure("TFrame", background="#e9ecef")
        style.configure("TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 10))
        style.configure("Title.TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 14, "bold"))
        style.configure("TEntry", font=("Roboto", 10), padding=3)
        style.configure("TCombobox", font=("Roboto", 10), padding=3)
        style.configure("TButton", font=("Roboto", 10, "bold"), padding=5)

        # Estilo para botões principais
        style.configure("Primary.TButton", background="#007bff", foreground="white",
                        bordercolor="#0056b3", lightcolor="#007bff", darkcolor="#0056b3")
        style.map("Primary.TButton",
                  background=[('active', '#0056b3'), ('!disabled', '#007bff')],
                  foreground=[('active', 'white'), ('!disabled', 'white')])

        # Estilo para botão de fechar
        style.configure("Cancel.TButton", background="#6c757d", foreground="white",
                        bordercolor="#5a6268", lightcolor="#6c757d", darkcolor="#5a6268")
        style.map("Cancel.TButton",
                  background=[('active', '#5a6268'), ('!disabled', '#6c757d')],
                  foreground=[('active', 'white'), ('!disabled', 'white')])

        # Estilo para botão do calendário
        style.configure("Calendar.TButton", background="#17a2b8", foreground="white",
                        bordercolor="#117a8b", lightcolor="#17a2b8", darkcolor="#117a8b")
        style.map("Calendar.TButton",
                  background=[('active', '#117a8b'), ('!disabled', '#17a2b8')],
                  foreground=[('active', 'white'), ('!disabled', 'white')])

    def _carregar_tipos_atendimento(self):
        """Carrega os tipos de atendimento (simplificado)"""
        self.todos_tipos = {
            "Consulta Médica": 1,
            "Exame Laboratorial": 2,
            "Atendimento Emergencial": 3
        }
        if hasattr(self, 'combo_tipo'):
            self.combo_tipo['values'] = list(self.todos_tipos.keys())

    def _setup_ui(self):
        """Configura a interface do usuário"""
        main_frame = ttk.Frame(self.root, padding="10")  # Padding reduzido
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self._criar_campos(main_frame)
        self._carregar_tipos_atendimento()

    def _criar_campos(self, parent):
        """Cria todos os campos do formulário"""
        # Título
        ttk.Label(parent, text="Novo Registro", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 10), sticky="w"
        )

        # Status
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        self.status_indicator = tk.Canvas(status_frame, width=16, height=16,
                                         bg="#e9ecef", highlightthickness=0)
        self.status_indicator.pack(side="left", padx=(0, 5))
        self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="#6c757d")
        ttk.Label(status_frame, text="Preencha os campos obrigatórios").pack(side="left")

        # Campos do formulário
        campos = [
            ("Data de Atendimento:", "entry_data", datetime.today().strftime("%d/%m/%Y")),
            ("Tipo de Atendimento:", "combo_tipo", []),
            ("Nível de Complexidade:", "combo_nivel", ["baixo", "médio", "grave", "gravíssimo"]),
            ("Número/Ticket:", "entry_ticket", ""),
            ("Status:", "combo_status", ["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"]),
            ("Descrição:", "txt_descricao", "")
        ]

        for row, (label, var_name, default) in enumerate(campos, start=2):
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky="e", pady=3, padx=5)

            if var_name == "combo_tipo":
                self.combo_tipo = ttk.Combobox(
                    parent,
                    textvariable=self.var_tipo,
                    state="normal",
                    width=30,  # Reduzido para compactar
                    font=("Roboto", 10)
                )
                self.combo_tipo.grid(row=row, column=1, pady=3, sticky="we", padx=5)
                self.combo_tipo.set("Digite para buscar...")

            elif var_name == "combo_nivel":
                self.combo_nivel = ttk.Combobox(parent, textvariable=self.var_nivel,
                                                values=default, state="readonly", width=30)
                self.combo_nivel.grid(row=row, column=1, pady=3, sticky="we", padx=5)
                self.combo_nivel.current(0)

            elif var_name == "entry_data":
                frame = ttk.Frame(parent)
                frame.grid(row=row, column=1, sticky="we", padx=5)
                self.entry_data = ttk.Entry(frame, width=15, font=("Roboto", 10))
                self.entry_data.insert(0, default)
                self.entry_data.pack(side="left")
                ttk.Button(frame, text="🗓️", command=self._abrir_calendario,
                           style="Calendar.TButton", width=3).pack(side="left", padx=5)

            elif var_name == "entry_ticket":
                self.entry_ticket = ttk.Entry(parent, width=30, font=("Roboto", 10))
                self.entry_ticket.grid(row=row, column=1, sticky="we", padx=5)

            elif var_name == "txt_descricao":
                self.txt_descricao = tk.Text(parent, height=3, width=30, wrap="word",
                                             font=("Roboto", 10))
                self.txt_descricao.grid(row=row, column=1, pady=3, sticky="we", padx=5)

            elif var_name == "combo_status":
                self.combo_status = ttk.Combobox(
                    parent,
                    textvariable=self.var_status,
                    values=default,
                    state="readonly",
                    width=30,
                    font=("Roboto", 10)
                )
                self.combo_status.grid(row=row, column=1, pady=3, sticky="we", padx=5)

        # Frame para botões
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=10, sticky="e")
        ttk.Button(
            button_frame,
            text="Salvar (Ctrl+Enter)",
            command=self._salvar,
            style="Primary.TButton"
        ).pack(side="right", padx=5)
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self._fechar_janela,
            style="Cancel.TButton"
        ).pack(side="right", padx=5)

    def _abrir_calendario(self):
        """Abre o calendário para seleção de data"""
        top = tk.Toplevel(self.root)
        top.title("Selecione a Data")
        top.transient(self.root)
        top.grab_set()
        top.minsize(250, 250)

        cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy", font=("Roboto", 9))
        cal.pack(pady=10, padx=10)

        ttk.Button(top, text="Selecionar", command=lambda: self._selecionar_data(cal, top),
                   style="Primary.TButton").pack(pady=5)

    def _selecionar_data(self, cal, top):
        """Processa a data selecionada no calendário"""
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, cal.get_date())
        top.destroy()

    def _preencher_campos(self, dados):
        """Preenche todos os campos com os dados iniciais"""
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, dados.get('data', ''))

        self.combo_tipo.set(dados.get('tipo', ''))
        self.combo_nivel.set(dados.get('nivel', 'baixo'))

        self.entry_ticket.delete(0, tk.END)
        self.entry_ticket.insert(0, dados.get('ticket', ''))

        self.txt_descricao.delete("1.0", tk.END)
        self.txt_descricao.insert("1.0", dados.get('descricao', '').strip())

        if 'status' in dados and dados['status'] is not None:
            self.combo_status.set(dados['status'])

    def _salvar(self):
        """Método para salvar os dados"""
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!", parent=self.root)

    def _fechar_janela(self):
        """Fecha a janela flutuante"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    app = RegistroFlutuante(root, colaborador="Teste")
    root.mainloop()