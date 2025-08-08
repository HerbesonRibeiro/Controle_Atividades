# # Revisado Conexão com o db
# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime
# import logging
# from tkcalendar import Calendar
# from utils.db import Database
#
#
# class RegistroFlutuante:
#     def __init__(self, master, colaborador, dados_iniciais=None):
#         """Inicializa a janela flutuante de forma confiável"""
#         try:
#             # Cria a janela Toplevel (Nova Janela)
#             self.root = tk.Toplevel(master)
#             self.root.title("Registro Flutuante")
#             self.root.minsize(400, 300)  # Tamanho inicial compacto
#             # Mantém a janela sempre no topo
#             self.root.attributes('-topmost', True)
#             # Configurações essenciais
#             self.root.transient(master)  # Torna dependente da principal
#             self.root.grab_set()  # Modal
#             # Conexão com o DB
#             self.db = Database()
#             # Centralizar a Janela
#             self._centralizar_janela()
#
#             self.colaborador = colaborador
#             self.var_tipo = tk.StringVar()
#             self.var_nivel = tk.StringVar()
#             self.var_status = tk.StringVar()
#             self.todos_tipos = {}  # Inicializa o dicionário de tipos
#
#             self._configurar_estilos()
#             self._setup_ui()
#             self._carregar_tipos_atendimento()  # Carrega os tipos após criar a UI
#
#             if dados_iniciais:
#                 self._preencher_campos(dados_iniciais)
#
#             self.root.after(100, self._verificar_visibilidade)
#
#             # Bind Ctrl+Enter para salvar
#             self.root.bind("<Control-Return>", lambda e: self._salvar())
#             self.root.bind("<Escape>", lambda e: self._fechar_janela())
#
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             raise RuntimeError(f"Falha ao inicializar janela flutuante: {str(e)}")
#
#     def _verificar_visibilidade(self):
#         if not self.root.winfo_viewable():
#             self.root.deiconify()
#             self.root.lift()
#             self.root.after(100, self._verificar_visibilidade)
#
#     def _centralizar_janela(self):
#         self.root.update_idletasks()
#         width = 500
#         height = 400
#         x = (self.root.winfo_screenwidth() // 2) - (width // 2)
#         y = (self.root.winfo_screenheight() // 2) - (height // 2)
#         self.root.geometry(f'{width}x{height}+{x}+{y}')
#
#     def _configurar_estilos(self):
#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("TFrame", background="#e9ecef")
#         style.configure("TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 10))
#         style.configure("Title.TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 14, "bold"))
#         style.configure("TEntry", font=("Roboto", 10), padding=3)
#         style.configure("TCombobox", font=("Roboto", 10), padding=3)
#         style.configure("TButton", font=("Roboto", 10, "bold"), padding=5)
#         style.configure("Primary.TButton", background="#007bff", foreground="white")
#         style.map("Primary.TButton",
#                   background=[('active', '#0056b3'), ('!disabled', '#007bff')],
#                   foreground=[('active', 'white'), ('!disabled', 'white')])
#         style.configure("Calendar.TButton", background="#17a2b8", foreground="white")
#         style.map("Calendar.TButton",
#                   background=[('active', '#117a8b'), ('!disabled', '#17a2b8')],
#                   foreground=[('active', 'white'), ('!disabled', 'white')])
#
#     def _carregar_tipos_atendimento(self):
#         try:
#             with self.db.get_connection() as conn:
#                 with conn.cursor(dictionary=True) as cursor:
#                     cursor.execute("SELECT id, nome FROM tipos_atendimento ORDER BY nome")
#                     tipos = cursor.fetchall()
#
#             self.todos_tipos = {row['nome']: row['id'] for row in tipos}
#
#             if hasattr(self, 'combo_tipo'):
#                 current_value = self.combo_tipo.get()
#                 self.combo_tipo['values'] = list(self.todos_tipos.keys())
#                 if not current_value or current_value == "Digite para buscar...":
#                     self.combo_tipo.set("Digite para buscar...")
#                 else:
#                     self.combo_tipo.set(current_value)
#
#         except Exception as e:
#             logging.error(f"Erro ao carregar tipos de atendimento: {e}")
#             self.todos_tipos = {
#                 "Teste erro 1": 1,
#                 "Teste erro 2": 2,
#                 "Teste erro 3": 3
#             }
#             if hasattr(self, 'combo_tipo'):
#                 self.combo_tipo['values'] = list(self.todos_tipos.keys())
#                 self.combo_tipo.set("Digite para buscar...")
#
#     def _setup_ui(self):
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.grid(row=0, column=0, sticky="nsew")
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#
#         ttk.Label(main_frame, text="Registro de Atividade", style="Title.TLabel").grid(
#             row=0, column=0, columnspan=2, pady=(0, 10), sticky="w"
#         )
#
#         status_frame = ttk.Frame(main_frame)
#         status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
#         self.status_indicator = tk.Canvas(status_frame, width=16, height=16,
#                                          bg="#e9ecef", highlightthickness=0)
#         self.status_indicator.pack(side="left", padx=(0, 5))
#         self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="#6c757d")
#         ttk.Label(status_frame, text="Preencha os campos obrigatórios").pack(side="left")
#
#         campos = [
#             ("Data de Atendimento:", "entry_data", datetime.today().strftime("%d/%m/%Y")),
#             ("Tipo de Atendimento:", "combo_tipo", []),
#             ("Nível de Complexidade:", "combo_nivel", ["BAIXO", "MÉDIO", "GRAVE", "GRAVÍSSIMO"]),
#             ("Número/Ticket:", "entry_ticket", ""),
#             ("Status:", "combo_status", ["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"]),
#             ("Descrição:", "txt_descricao", "")
#         ]
#
#         for row, (label, var_name, default) in enumerate(campos, start=2):
#             ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="e", pady=3, padx=5)
#             if var_name == "combo_tipo":
#                 self.combo_tipo = ttk.Combobox(main_frame, textvariable=self.var_tipo, state="normal", width=30, font=("Roboto", 10))
#                 self.combo_tipo.grid(row=row, column=1, pady=3, sticky="we", padx=5)
#                 self.combo_tipo.set("Digite para buscar...")
#             elif var_name == "combo_nivel":
#                 self.combo_nivel = ttk.Combobox(main_frame, textvariable=self.var_nivel, values=default, state="readonly", width=30)
#                 self.combo_nivel.grid(row=row, column=1, pady=3, sticky="we", padx=5)
#                 self.combo_nivel.current(0)
#             elif var_name == "entry_data":
#                 frame = ttk.Frame(main_frame)
#                 frame.grid(row=row, column=1, sticky="we", padx=5)
#                 self.entry_data = ttk.Entry(frame, width=15, font=("Roboto", 10))
#                 self.entry_data.insert(0, default)
#                 self.entry_data.pack(side="left")
#                 ttk.Button(frame, text="🗓️", command=self._abrir_calendario, style="Calendar.TButton", width=3).pack(side="left", padx=5)
#             elif var_name == "entry_ticket":
#                 self.entry_ticket = ttk.Entry(main_frame, width=30, font=("Roboto", 10))
#                 self.entry_ticket.grid(row=row, column=1, sticky="we", padx=5)
#             elif var_name == "txt_descricao":
#                 self.txt_descricao = tk.Text(main_frame, height=3, width=30, wrap="word", font=("Roboto", 10))
#                 self.txt_descricao.grid(row=row, column=1, pady=3, sticky="we", padx=5)
#             elif var_name == "combo_status":
#                 self.combo_status = ttk.Combobox(main_frame, textvariable=self.var_status, values=default, state="readonly", width=30, font=("Roboto", 10))
#                 self.combo_status.grid(row=row, column=1, pady=3, sticky="we", padx=5)
#
#         button_frame = ttk.Frame(main_frame)
#         button_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=10, sticky="e")
#
#         self.btn_salvar = ttk.Button(button_frame, text="Salvar (Ctrl+Enter)", command=self._salvar, style="Primary.TButton")
#         self.btn_salvar.pack(side="right", padx=5)
#
#     def _abrir_calendario(self):
#         top = tk.Toplevel(self.root)
#         top.title("Selecione a Data")
#         top.transient(self.root)
#         top.grab_set()
#         top.minsize(250, 250)
#
#         cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy", font=("Roboto", 9))
#         cal.pack(pady=10, padx=10)
#
#         ttk.Button(top, text="Selecionar", command=lambda: self._selecionar_data(cal, top), style="Primary.TButton").pack(pady=5)
#
#     def _selecionar_data(self, cal, top):
#         self.entry_data.delete(0, tk.END)
#         self.entry_data.insert(0, cal.get_date())
#         top.destroy()
#
#     def _preencher_campos(self, dados):
#         self.entry_data.delete(0, tk.END)
#         self.entry_data.insert(0, dados.get('data', ''))
#         self.combo_tipo.set(dados.get('tipo', ''))
#         self.combo_nivel.set(dados.get('nivel', 'baixo'))
#         self.entry_ticket.delete(0, tk.END)
#         self.entry_ticket.insert(0, dados.get('ticket', ''))
#         self.txt_descricao.delete("1.0", tk.END)
#         self.txt_descricao.insert("1.0", dados.get('descricao', '').strip())
#         if 'status' in dados and dados['status'] is not None:
#             self.combo_status.set(dados['status'])
#
#     def _salvar(self):
#         try:
#             if hasattr(self, 'btn_salvar'):
#                 self.btn_salvar.config(state=tk.DISABLED, text="Salvando...")
#
#             erros = []
#             if not self.var_tipo.get() or self.var_tipo.get() == "Digite para buscar...":
#                 erros.append("Selecione um tipo de atendimento")
#             if not self.entry_data.get():
#                 erros.append("Informe a data do atendimento")
#
#             if erros:
#                 raise ValueError("\n• " + "\n• ".join(erros))
#
#             try:
#                 data_db = datetime.strptime(self.entry_data.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
#             except ValueError:
#                 raise ValueError("Data inválida. Use o formato DD/MM/AAAA")
#
#             dados = {
#                 "colaborador_id": self.colaborador.id,
#                 "data_atendimento": data_db,
#                 "tipo_atendimento_id": self.todos_tipos[self.var_tipo.get()],
#                 "nivel_complexidade": self.var_nivel.get().upper(),
#                 "numero_atendimento": self.entry_ticket.get().strip() or None,
#                 "descricao": self.txt_descricao.get("1.0", "end-1c").strip(),
#                 "status": self.var_status.get().strip().upper()
#             }
#
#             with self.db.get_connection() as conn:
#                 with conn.cursor() as cursor:
#                     cursor.execute("""
#                         INSERT INTO atividades (
#                             colaborador_id, data_atendimento, tipo_atendimento_id,
#                             nivel_complexidade, numero_atendimento, descricao,
#                             status
#                         ) VALUES (%s, %s, %s, %s, %s, %s, %s)
#                     """, tuple(dados.values()))
#                 conn.commit()
#
#             messagebox.showinfo("Sucesso", "Registro salvo com sucesso!", parent=self.root)
#             self._limpar_formulario()
#             self._atualizar_status("sucesso")
#
#         except ValueError as ve:
#             self._atualizar_status("erro")
#             messagebox.showerror("Erro de Validação", str(ve), parent=self.root)
#         except Exception as e:
#             self._atualizar_status("erro")
#             logging.error(f"Erro ao salvar: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Erro ao salvar no banco de dados.\n{str(e)}", parent=self.root)
#         finally:
#             if hasattr(self, 'btn_salvar'):
#                 self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")
#
#     def _fechar_janela(self):
#         self.root.destroy()
#
#     def _limpar_formulario(self):
#         self.entry_data.delete(0, tk.END)
#         self.entry_data.insert(0, datetime.today().strftime('%d/%m/%Y'))
#         self.combo_tipo.set('')
#         self.combo_tipo.insert(0, "Digite para buscar...")
#         self.var_nivel.set("baixo")
#         self.entry_ticket.delete(0, tk.END)
#         self.txt_descricao.delete("1.0", tk.END)
#         self._atualizar_status("padrao")
#         self.var_status.set("RESOLVIDO")
#
#     def _atualizar_status(self, estado="padrao"):
#         cores = {
#             "padrao": "#6c757d",
#             "editando": "#17a2b8",
#             "sucesso": "#28a745",
#             "erro": "#dc3545",
#         }
#         if hasattr(self, 'status_circle'):
#             self.status_indicator.itemconfig(self.status_circle, fill=cores.get(estado, "#6c757d"))

# Revisado Conexão com o db
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
from tkcalendar import Calendar
from utils.db import Database


class RegistroFlutuante:
    def __init__(self, master, colaborador, dados_iniciais=None):
        """Inicializa a janela flutuante de forma confiável"""
        try:
            self.root = tk.Toplevel(master)
            self.root.title("Registro Flutuante")
            self.root.minsize(400, 300)
            self.root.attributes('-topmost', True)
            self.root.transient(master)
            self.root.grab_set()
            self.db = Database()
            self._centralizar_janela()

            self.colaborador = colaborador
            self.var_tipo = tk.StringVar()
            self.var_nivel = tk.StringVar()
            self.var_status = tk.StringVar()
            self.todos_tipos = {}

            self._configurar_estilos()
            self._setup_ui()
            self._carregar_tipos_atendimento()

            if dados_iniciais:
                self._preencher_campos(dados_iniciais)

            self.root.after(100, self._verificar_visibilidade)
            self.root.bind("<Control-Return>", lambda e: self._salvar())
            self.root.bind("<Escape>", lambda e: self._fechar_janela())

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Falha ao inicializar janela flutuante: {str(e)}")

    def _verificar_visibilidade(self):
        if not self.root.winfo_viewable():
            self.root.deiconify()
            self.root.lift()
            self.root.after(100, self._verificar_visibilidade)

    def _centralizar_janela(self):
        self.root.update_idletasks()
        width = 500
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#e9ecef")
        style.configure("TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 10))
        style.configure("Title.TLabel", background="#e9ecef", foreground="#212529", font=("Roboto", 14, "bold"))
        style.configure("TEntry", font=("Roboto", 10), padding=3)
        style.configure("TCombobox", font=("Roboto", 10), padding=3)
        style.configure("TButton", font=("Roboto", 10, "bold"), padding=5)
        style.configure("Primary.TButton", background="#007bff", foreground="white")
        style.map("Primary.TButton",
                  background=[('active', '#0056b3'), ('!disabled', '#007bff')],
                  foreground=[('active', 'white'), ('!disabled', 'white')])
        style.configure("Calendar.TButton", background="#17a2b8", foreground="white")
        style.map("Calendar.TButton",
                  background=[('active', '#117a8b'), ('!disabled', '#17a2b8')],
                  foreground=[('active', 'white'), ('!disabled', 'white')])

    def _carregar_tipos_atendimento(self):
        try:
            # <<< SUGESTÃO APLICADA: Usando o método centralizado execute_query >>>
            query = "SELECT id, nome FROM tipos_atendimento ORDER BY nome"
            tipos = self.db.execute_query(query)

            self.todos_tipos = {row['nome']: row['id'] for row in tipos}

            if hasattr(self, 'combo_tipo'):
                current_value = self.combo_tipo.get()
                self.combo_tipo['values'] = list(self.todos_tipos.keys())
                if not current_value or current_value == "Digite para buscar...":
                    self.combo_tipo.set("Digite para buscar...")
                else:
                    self.combo_tipo.set(current_value)

        except Exception as e:
            logging.error(f"Erro ao carregar tipos de atendimento: {e}")
            self.todos_tipos = {
                "Teste erro 1": 1,
                "Teste erro 2": 2,
                "Teste erro 3": 3
            }
            if hasattr(self, 'combo_tipo'):
                self.combo_tipo['values'] = list(self.todos_tipos.keys())
                self.combo_tipo.set("Digite para buscar...")

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Registro de Atividade", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 10), sticky="w"
        )

        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        self.status_indicator = tk.Canvas(status_frame, width=16, height=16,
                                          bg="#e9ecef", highlightthickness=0)
        self.status_indicator.pack(side="left", padx=(0, 5))
        self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="#6c757d")
        ttk.Label(status_frame, text="Preencha os campos obrigatórios").pack(side="left")

        campos = [
            ("Data de Atendimento:", "entry_data", datetime.today().strftime("%d/%m/%Y")),
            ("Tipo de Atendimento:", "combo_tipo", []),
            ("Nível de Complexidade:", "combo_nivel", ["BAIXO", "MÉDIO", "GRAVE", "GRAVÍSSIMO"]),
            ("Número/Ticket:", "entry_ticket", ""),
            ("Status:", "combo_status", ["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"]),
            ("Descrição:", "txt_descricao", "")
        ]

        for row, (label, var_name, default) in enumerate(campos, start=2):
            ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="e", pady=3, padx=5)
            if var_name == "combo_tipo":
                self.combo_tipo = ttk.Combobox(main_frame, textvariable=self.var_tipo, state="normal", width=30,
                                               font=("Roboto", 10))
                self.combo_tipo.grid(row=row, column=1, pady=3, sticky="we", padx=5)
                self.combo_tipo.set("Digite para buscar...")
            elif var_name == "combo_nivel":
                self.combo_nivel = ttk.Combobox(main_frame, textvariable=self.var_nivel, values=default,
                                                state="readonly", width=30)
                self.combo_nivel.grid(row=row, column=1, pady=3, sticky="we", padx=5)
                self.combo_nivel.current(0)
            elif var_name == "entry_data":
                frame = ttk.Frame(main_frame)
                frame.grid(row=row, column=1, sticky="we", padx=5)
                self.entry_data = ttk.Entry(frame, width=15, font=("Roboto", 10))
                self.entry_data.insert(0, default)
                self.entry_data.pack(side="left")
                ttk.Button(frame, text="🗓️", command=self._abrir_calendario, style="Calendar.TButton", width=3).pack(
                    side="left", padx=5)
            elif var_name == "entry_ticket":
                self.entry_ticket = ttk.Entry(main_frame, width=30, font=("Roboto", 10))
                self.entry_ticket.grid(row=row, column=1, sticky="we", padx=5)
            elif var_name == "txt_descricao":
                self.txt_descricao = tk.Text(main_frame, height=3, width=30, wrap="word", font=("Roboto", 10))
                self.txt_descricao.grid(row=row, column=1, pady=3, sticky="we", padx=5)
            elif var_name == "combo_status":
                self.combo_status = ttk.Combobox(main_frame, textvariable=self.var_status, values=default,
                                                 state="readonly", width=30, font=("Roboto", 10))
                self.combo_status.grid(row=row, column=1, pady=3, sticky="we", padx=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=10, sticky="e")

        self.btn_salvar = ttk.Button(button_frame, text="Salvar (Ctrl+Enter)", command=self._salvar,
                                     style="Primary.TButton")
        self.btn_salvar.pack(side="right", padx=5)

    def _abrir_calendario(self):
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
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, cal.get_date())
        top.destroy()

    def _preencher_campos(self, dados):
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
        try:
            if hasattr(self, 'btn_salvar'):
                self.btn_salvar.config(state=tk.DISABLED, text="Salvando...")

            erros = []
            if not self.var_tipo.get() or self.var_tipo.get() == "Digite para buscar...":
                erros.append("Selecione um tipo de atendimento")
            if not self.entry_data.get():
                erros.append("Informe a data do atendimento")

            if erros:
                raise ValueError("\n• " + "\n• ".join(erros))

            try:
                data_db = datetime.strptime(self.entry_data.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("Data inválida. Use o formato DD/MM/AAAA")

            dados = {
                "colaborador_id": self.colaborador.id,
                "data_atendimento": data_db,
                "tipo_atendimento_id": self.todos_tipos[self.var_tipo.get()],
                "nivel_complexidade": self.var_nivel.get().upper(),
                "numero_atendimento": self.entry_ticket.get().strip() or None,
                "descricao": self.txt_descricao.get("1.0", "end-1c").strip(),
                "status": self.var_status.get().strip().upper()
            }

            # <<< SUGESTÃO APLICADA: Usando o método centralizado execute_query >>>
            query = """
                INSERT INTO atividades (
                    colaborador_id, data_atendimento, tipo_atendimento_id,
                    nivel_complexidade, numero_atendimento, descricao,
                    status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, params=tuple(dados.values()), fetch=False)

            messagebox.showinfo("Sucesso", "Registro salvo com sucesso!", parent=self.root)
            self._limpar_formulario()
            self._atualizar_status("sucesso")

        except ValueError as ve:
            self._atualizar_status("erro")
            messagebox.showerror("Erro de Validação", str(ve), parent=self.root)
        except Exception as e:
            self._atualizar_status("erro")
            logging.error(f"Erro ao salvar: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados.\n{str(e)}", parent=self.root)
        finally:
            if hasattr(self, 'btn_salvar'):
                self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")

    def _fechar_janela(self):
        self.root.destroy()

    def _limpar_formulario(self):
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.today().strftime('%d/%m/%Y'))
        self.combo_tipo.set('')
        self.combo_tipo.insert(0, "Digite para buscar...")
        self.var_nivel.set("baixo")
        self.entry_ticket.delete(0, tk.END)
        self.txt_descricao.delete("1.0", tk.END)
        self._atualizar_status("padrao")
        self.var_status.set("RESOLVIDO")

    def _atualizar_status(self, estado="padrao"):
        cores = {
            "padrao": "#6c757d",
            "editando": "#17a2b8",
            "sucesso": "#28a745",
            "erro": "#dc3545",
        }
        if hasattr(self, 'status_circle'):
            self.status_indicator.itemconfig(self.status_circle, fill=cores.get(estado, "#6c757d"))