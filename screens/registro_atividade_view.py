# ## Revisado conexão com o db
# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime
# from tkcalendar import Calendar
# from utils.db import Database
# import logging
# import re
#
#
# class RegistroAtividadeView:
#     def __init__(self, master, colaborador):
#         self.master = master
#         self.colaborador = colaborador
#         self.db = Database()
#         self.todos_tipos = {}
#         self._after_id = None
#
#         self._configurar_estilos()
#         self._setup_ui()
#         self._carregar_tipos_atendimento()
#         self._configurar_atalhos()
#         self.combo_tipo.bind('<Escape>', self._limpar_busca)
#
#     def _configurar_estilos(self):
#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("TFrame", background="#f8f9fa")
#         style.configure("TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 10))
#         style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 18, "bold"))
#         style.configure("TEntry", font=("Segoe UI", 10))
#         style.configure("TButton", font=("Segoe UI", 10, "bold"))
#         style.configure("TCombobox", font=("Segoe UI", 10))
#         style.configure("Primary.TButton", background="#4a6da7", foreground="white",
#                         font=("Segoe UI", 10, "bold"), padding=6)
#         style.map("Primary.TButton", background=[("active", "#3a5a8a")])
#         style.configure("Calendar.TButton", background="#dee2e6", foreground="#343a40",
#                         font=("Segoe UI", 9), padding=5, relief="flat")
#         style.map("Calendar.TButton", background=[("active", "#ced4da")])
#         style.configure("Flutuante.TButton", background="#6c757d", foreground="white",
#                         font=("Segoe UI", 10, "bold"), padding=6)
#         style.map("Flutuante.TButton", background=[("active", "#5a6268")])
#
#     def _configurar_atalhos(self):
#         self.master.bind("<Control-Return>", lambda e: self._salvar())
#         self.master.bind("<Escape>", lambda e: self.master.destroy())
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
#                 self.combo_tipo['values'] = list(self.todos_tipos.keys())
#                 self.combo_tipo.set("Digite para buscar...")
#
#         except Exception as e:
#             print(f"ERRO no carregamento: {e}")
#             self.todos_tipos = {
#                 "Teste erro 1": 1,
#                 "Teste erro 2": 2,
#                 "Teste erro 3": 3
#             }
#             if hasattr(self, 'combo_tipo'):
#                 self.combo_tipo['values'] = list(self.todos_tipos.keys())
#
#     def _on_combo_focus(self, event=None):
#         if self.combo_tipo.get() == "Digite para buscar...":
#             self.combo_tipo.set('')
#             self.combo_tipo['values'] = list(self.todos_tipos.keys())
#
#     def _filtrar_tipos_debounce(self, event):
#         current_text = self.combo_tipo.get()
#         if current_text == "Digite para buscar...":
#             return
#         if event.keysym in ('Return', 'Up', 'Down', 'Left', 'Right', 'Escape', 'Tab'):
#             return
#
#         if self._after_id:
#             try:
#                 self.master.after_cancel(self._after_id)
#             except (ValueError, tk.TclError):
#                 pass
#             finally:
#                 self._after_id = None
#
#         self._after_id = self.master.after(300, self._executar_filtro)
#
#     def _executar_filtro(self):
#         self._after_id = None
#         texto = self.combo_tipo.get()
#         if not texto:
#             self.combo_tipo['values'] = list(self.todos_tipos.keys())
#             return
#
#         texto_lower = texto.lower()
#         valores_filtrados = [item for item in self.todos_tipos.keys() if texto_lower in item.lower()][:50]
#
#         current_position = self.combo_tipo.index(tk.INSERT)
#         self.combo_tipo['values'] = valores_filtrados
#         self.combo_tipo.set(texto)
#         self.combo_tipo.icursor(current_position)
#
#         if valores_filtrados:
#             self.combo_tipo.event_generate('<Down>')
#
#     def _abrir_calendario(self):
#         top = tk.Toplevel(self.master)
#         top.title("Selecione a Data")
#         top.resizable(False, False)
#
#         cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy")
#         cal.pack(pady=10)
#
#         def set_date():
#             self.entry_data.delete(0, tk.END)
#             self.entry_data.insert(0, cal.get_date())
#             top.destroy()
#             self._atualizar_status("editando")
#
#         ttk.Button(top, text="Selecionar", command=set_date, style="Primary.TButton").pack(pady=5)
#
#         top.update_idletasks()
#         w = top.winfo_width()
#         h = top.winfo_height()
#         x = (top.winfo_screenwidth() // 2) - (w // 2)
#         y = (top.winfo_screenheight() // 2) - (h // 2)
#         top.geometry(f"{w}x{h}+{x}+{y}")
#
#     def _setup_ui(self):
#         main_frame = ttk.Frame(self.master, padding=(20, 15))
#         main_frame.pack(expand=True, fill="both")
#
#         ttk.Label(main_frame, text="📄 Registro de Atividades", style="Title.TLabel").grid(
#             row=0, column=0, columnspan=2, pady=(0, 10))
#
#         status_frame = ttk.Frame(main_frame)
#         status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
#
#         self.status_indicator = tk.Canvas(status_frame, width=16, height=16,
#                                           bg="#f8f9fa", highlightthickness=0)
#         self.status_indicator.pack(side="left", padx=(0, 5))
#         self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="gray")
#         ttk.Label(status_frame, text="Preencha os campos obrigatórios").pack(side="left")
#
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
#             ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="e", pady=4, padx=5)
#
#             if var_name == "combo_tipo":
#                 self.var_tipo = tk.StringVar()
#                 self.combo_tipo = ttk.Combobox(
#                     main_frame,
#                     textvariable=self.var_tipo,
#                     state="normal",
#                     width=40,
#                     font=("Segoe UI", 10)
#                 )
#                 self.combo_tipo.grid(row=row, column=1, pady=4, sticky="we", padx=5)
#                 self.combo_tipo.set("Digite para buscar...")
#
#             elif var_name == "combo_nivel":
#                 self.var_nivel = tk.StringVar()
#                 self.combo_nivel = ttk.Combobox(main_frame, textvariable=self.var_nivel,
#                                                 values=default, state="readonly")
#                 self.combo_nivel.grid(row=row, column=1, pady=4, sticky="we")
#                 self.combo_nivel.current(0)
#
#             elif var_name == "entry_data":
#                 frame = ttk.Frame(main_frame)
#                 frame.grid(row=row, column=1, sticky="we")
#                 self.entry_data = ttk.Entry(frame, width=15)
#                 self.entry_data.insert(0, default)
#                 self.entry_data.pack(side="left")
#                 ttk.Button(frame, text="🗓️ Escolher", command=self._abrir_calendario,
#                            style="Calendar.TButton").pack(side="left", padx=8)
#
#             elif var_name == "entry_ticket":
#                 self.entry_ticket = ttk.Entry(main_frame)
#                 self.entry_ticket.grid(row=row, column=1, sticky="we")
#
#             elif var_name == "txt_descricao":
#                 self.txt_descricao = tk.Text(main_frame, height=4, width=40, wrap="word")
#                 self.txt_descricao.grid(row=row, column=1, pady=4, sticky="we")
#
#             elif var_name == "combo_status":
#                 self.var_status = tk.StringVar(value="RESOLVIDO")
#                 self.combo_status = ttk.Combobox(
#                     main_frame,
#                     textvariable=self.var_status,
#                     values=default,
#                     state="readonly"
#                 )
#                 self.combo_status.grid(row=row, column=1, pady=4, sticky="we")
#
#         btn_frame = ttk.Frame(main_frame)
#         btn_frame.grid(row=8, column=0, columnspan=2, pady=15)
#
#         self.btn_salvar = ttk.Button(btn_frame, text="Salvar (Ctrl+Enter)",
#                                      command=self._salvar, style="Primary.TButton")
#         self.btn_salvar.pack(side="left", padx=5)
#         ttk.Button(btn_frame, text="Limpar", command=self._limpar_formulario).pack(side="left", padx=5)
#         main_frame.columnconfigure(1, weight=1, minsize=250)
#
#         btn_flutuante = ttk.Button(
#             btn_frame,
#             text="Abrir em Janela Flutuante",
#             command=self._abrir_flutuante,
#             style="Flutuante.TButton"
#         )
#         btn_flutuante.pack(side=tk.LEFT, padx=5)
#
#         self._configurar_bindings()
#
#     def _configurar_bindings(self):
#         self.combo_tipo.bind('<KeyRelease>', self._filtrar_tipos_debounce)
#         self.combo_tipo.bind('<FocusIn>', self._on_combo_focus)
#         self.combo_tipo.bind('<Escape>', self._limpar_busca)
#         self.combo_tipo.bind('<<ComboboxSelected>>', self._tipo_selecionado)
#
#     def _atualizar_status(self, estado):
#         cores = {
#             "editando": "yellow",
#             "sucesso": "green",
#             "erro": "red",
#             "padrao": "gray"
#         }
#         self.status_indicator.itemconfig(self.status_circle, fill=cores.get(estado, "gray"))
#
#     def _validar_dados(self):
#         erros = []
#         data = self.entry_data.get()
#
#         if not re.match(r"^\d{2}/\d{2}/\d{4}$", data):
#             erros.append("Formato de data inválido (DD/MM/AAAA)")
#         else:
#             try:
#                 datetime.strptime(data, "%d/%m/%Y")
#             except ValueError:
#                 erros.append("Data inválida ou inexistente")
#
#         tipo = self.var_tipo.get()
#         if not tipo or tipo == "Digite para buscar...":
#             erros.append("Tipo de atendimento obrigatório")
#         elif tipo not in self.todos_tipos:
#             erros.append("Selecione um tipo de atendimento válido da lista")
#
#         descricao = self.txt_descricao.get("1.0", "end-1c").strip()
#         if not descricao:
#             erros.append("Descrição obrigatória")
#         elif len(descricao) < 1:
#             erros.append("Descrição muito curta (mínimo 1 caracteres)")
#
#         return erros
#
#     def _salvar(self):
#         self.btn_salvar.config(state=tk.DISABLED, text="Salvando...")
#         self._atualizar_status("editando")
#
#         try:
#             erros = self._validar_dados()
#             if erros:
#                 raise ValueError("\n• " + "\n• ".join(erros))
#
#             data_db = datetime.strptime(self.entry_data.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
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
#             messagebox.showinfo("Sucesso", "Registro salvo com sucesso!", parent=self.master)
#             self._limpar_formulario()
#             self._atualizar_status("sucesso")
#
#             self.btn_salvar.config(text="Salvo ✓")
#             self.master.after(1200, lambda: self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)"))
#
#         except ValueError as ve:
#             self._atualizar_status("erro")
#             messagebox.showerror("Erro de Validação", str(ve))
#             self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")
#
#         except Exception as e:
#             self._atualizar_status("erro")
#             logging.error(f"Erro ao salvar: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Erro ao salvar no banco de dados.\n{str(e)}")
#             self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")
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
#     def _limpar_busca(self, event=None):
#         self.combo_tipo.set('')
#         self.combo_tipo['values'] = list(self.todos_tipos.keys())
#         return "break"
#
#     def _tipo_selecionado(self, event):
#         if self.var_tipo.get() not in self.todos_tipos:
#             self.var_tipo.set('')
#         self._atualizar_status("editando")
#
#     def _abrir_flutuante(self):
#         try:
#             dados = {
#                 'data': self.entry_data.get(),
#                 'tipo': self.var_tipo.get(),
#                 'nivel': self.var_nivel.get(),
#                 'ticket': self.entry_ticket.get().strip(),
#                 'descricao': self.txt_descricao.get("1.0", tk.END).strip(),
#                 'status': self.var_status.get() if hasattr(self, 'var_status') else None
#             }
#
#             root_window = self.master.winfo_toplevel()
#
#             try:
#                 from screens.registro_atividade_flutuante_view import RegistroFlutuante
#             except ImportError:
#                 try:
#                     from registro_atividade_flutuante_view import RegistroFlutuante
#                 except ImportError as e:
#                     messagebox.showerror("Erro", f"Não foi possível carregar a janela flutuante: {str(e)}",
#                                          parent=root_window)
#                     return
#
#             self.flutuante = RegistroFlutuante(root_window, self.colaborador, dados)
#
#             if not hasattr(self.flutuante, 'root') or not self.flutuante.root.winfo_exists():
#                 messagebox.showerror("Erro", "Falha ao criar a janela flutuante", parent=root_window)
#                 return
#
#             self.flutuante.root.protocol("WM_DELETE_WINDOW", self._fechar_flutuante)
#
#             root_window.withdraw()
#
#             self.flutuante.root.focus_force()
#             self.flutuante.root.lift()
#
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             self.master.winfo_toplevel().deiconify()
#             messagebox.showerror("Erro", f"Falha ao abrir janela flutuante:\n{str(e)}", parent=self.master)
#
#     def _fechar_flutuante(self):
#         try:
#             if hasattr(self, 'flutuante'):
#                 try:
#                     if self.flutuante.root.winfo_exists():
#                         self.flutuante.root.destroy()
#                 except tk.TclError:
#                     pass
#                 del self.flutuante
#         finally:
#             root_window = self.master.winfo_toplevel()
#             root_window.deiconify()
#             root_window.focus_force()

## Revisado conexão com o db
'''importtkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
from utils.db import Database
import logging
import re


class RegistroAtividadeView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.db = Database()
        self.todos_tipos = {}
        self._after_id = None

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_tipos_atendimento()
        self._configurar_atalhos()
        self.combo_tipo.bind('<Escape>', self._limpar_busca)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 18, "bold"))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TCombobox", font=("Segoe UI", 10))
        style.configure("Primary.TButton", background="#4a6da7", foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Primary.TButton", background=[("active", "#3a5a8a")])
        style.configure("Calendar.TButton", background="#dee2e6", foreground="#343a40",
                        font=("Segoe UI", 9), padding=5, relief="flat")
        style.map("Calendar.TButton", background=[("active", "#ced4da")])
        style.configure("Flutuante.TButton", background="#6c757d", foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Flutuante.TButton", background=[("active", "#5a6268")])

    def _configurar_atalhos(self):
        self.master.bind("<Control-Return>", lambda e: self._salvar())
        self.master.bind("<Escape>", lambda e: self.master.destroy())

    def _carregar_tipos_atendimento(self):
        try:
            # <<< SUGESTÃO APLICADA: Usando o método centralizado execute_query >>>
            # Simplifica a chamada ao banco de dados e aumenta a segurança.
            query = "SELECT id, nome FROM tipos_atendimento ORDER BY nome"
            tipos = self.db.execute_query(query)

            self.todos_tipos = {row['nome']: row['id'] for row in tipos}

            if hasattr(self, 'combo_tipo'):
                self.combo_tipo['values'] = list(self.todos_tipos.keys())
                self.combo_tipo.set("Digite para buscar...")

        except Exception as e:
            # Mantido seu excelente tratamento de erro para casos de falha de conexão.
            print(f"ERRO no carregamento: {e}")
            self.todos_tipos = {
                "Teste erro 1": 1,
                "Teste erro 2": 2,
                "Teste erro 3": 3
            }
            if hasattr(self, 'combo_tipo'):
                self.combo_tipo['values'] = list(self.todos_tipos.keys())

    def _on_combo_focus(self, event=None):
        if self.combo_tipo.get() == "Digite para buscar...":
            self.combo_tipo.set('')
            self.combo_tipo['values'] = list(self.todos_tipos.keys())

    def _filtrar_tipos_debounce(self, event):
        current_text = self.combo_tipo.get()
        if current_text == "Digite para buscar...":
            return
        if event.keysym in ('Return', 'Up', 'Down', 'Left', 'Right', 'Escape', 'Tab'):
            return

        if self._after_id:
            try:
                self.master.after_cancel(self._after_id)
            except (ValueError, tk.TclError):
                pass
            finally:
                self._after_id = None

        self._after_id = self.master.after(300, self._executar_filtro)

    def _executar_filtro(self):
        self._after_id = None
        texto = self.combo_tipo.get()
        if not texto:
            self.combo_tipo['values'] = list(self.todos_tipos.keys())
            return

        texto_lower = texto.lower()
        valores_filtrados = [item for item in self.todos_tipos.keys() if texto_lower in item.lower()][:50]

        current_position = self.combo_tipo.index(tk.INSERT)
        self.combo_tipo['values'] = valores_filtrados
        self.combo_tipo.set(texto)
        self.combo_tipo.icursor(current_position)

        if valores_filtrados:
            self.combo_tipo.event_generate('<Down>')

    def _abrir_calendario(self):
        top = tk.Toplevel(self.master)
        top.title("Selecione a Data")
        top.resizable(False, False)

        cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy")
        cal.pack(pady=10)

        def set_date():
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, cal.get_date())
            top.destroy()
            self._atualizar_status("editando")

        ttk.Button(top, text="Selecionar", command=set_date, style="Primary.TButton").pack(pady=5)

        top.update_idletasks()
        w = top.winfo_width()
        h = top.winfo_height()
        x = (top.winfo_screenwidth() // 2) - (w // 2)
        y = (top.winfo_screenheight() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")

    def _setup_ui(self):
        main_frame = ttk.Frame(self.master, padding=(20, 15))
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="📄 Registro de Atividades", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 10))

        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self.status_indicator = tk.Canvas(status_frame, width=16, height=16,
                                          bg="#f8f9fa", highlightthickness=0)
        self.status_indicator.pack(side="left", padx=(0, 5))
        self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="gray")
        ttk.Label(status_frame, text="Preencha os campos obrigatórios").pack(side="left")

        campos = [
            ("Data de Atendimento:", "entry_data", datetime.today().strftime("%d/%m/%Y")),
            ("Tipo de Atendimento:", "combo_tipo", []),
            ("Nível de Complexidade:", "combo_nivel", ["baixo", "medio", "grave", "gravissimo"]),
            ("Número/Ticket:", "entry_ticket", ""),
            ("Status:", "combo_status", ["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"]),
            ("Descrição:", "txt_descricao", "")
        ]

        for row, (label, var_name, default) in enumerate(campos, start=2):
            ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="e", pady=4, padx=5)

            if var_name == "combo_tipo":
                self.var_tipo = tk.StringVar()
                self.combo_tipo = ttk.Combobox(
                    main_frame,
                    textvariable=self.var_tipo,
                    state="normal",
                    width=40,
                    font=("Segoe UI", 10)
                )
                self.combo_tipo.grid(row=row, column=1, pady=4, sticky="we", padx=5)
                self.combo_tipo.set("Digite para buscar...")

            elif var_name == "combo_nivel":
                self.var_nivel = tk.StringVar()
                self.combo_nivel = ttk.Combobox(main_frame, textvariable=self.var_nivel,
                                                values=default, state="readonly")
                self.combo_nivel.grid(row=row, column=1, pady=4, sticky="we")
                self.combo_nivel.current(0)

            elif var_name == "entry_data":
                frame = ttk.Frame(main_frame)
                frame.grid(row=row, column=1, sticky="we")
                self.entry_data = ttk.Entry(frame, width=15)
                self.entry_data.insert(0, default)
                self.entry_data.pack(side="left")
                ttk.Button(frame, text="🗓️ Escolher", command=self._abrir_calendario,
                           style="Calendar.TButton").pack(side="left", padx=8)

            elif var_name == "entry_ticket":
                self.entry_ticket = ttk.Entry(main_frame)
                self.entry_ticket.grid(row=row, column=1, sticky="we")

            elif var_name == "txt_descricao":
                self.txt_descricao = tk.Text(main_frame, height=4, width=40, wrap="word")
                self.txt_descricao.grid(row=row, column=1, pady=4, sticky="we")

            elif var_name == "combo_status":
                self.var_status = tk.StringVar(value="RESOLVIDO")
                self.combo_status = ttk.Combobox(
                    main_frame,
                    textvariable=self.var_status,
                    values=default,
                    state="readonly"
                )
                self.combo_status.grid(row=row, column=1, pady=4, sticky="we")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=15)

        self.btn_salvar = ttk.Button(btn_frame, text="Salvar (Ctrl+Enter)",
                                     command=self._salvar, style="Primary.TButton")
        self.btn_salvar.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar_formulario).pack(side="left", padx=5)
        main_frame.columnconfigure(1, weight=1, minsize=250)

        btn_flutuante = ttk.Button(
            btn_frame,
            text="Abrir em Janela Flutuante",
            command=self._abrir_flutuante,
            style="Flutuante.TButton"
        )
        btn_flutuante.pack(side=tk.LEFT, padx=5)

        self._configurar_bindings()

    def _configurar_bindings(self):
        self.combo_tipo.bind('<KeyRelease>', self._filtrar_tipos_debounce)
        self.combo_tipo.bind('<FocusIn>', self._on_combo_focus)
        self.combo_tipo.bind('<Escape>', self._limpar_busca)
        self.combo_tipo.bind('<<ComboboxSelected>>', self._tipo_selecionado)

    def _atualizar_status(self, estado):
        cores = {
            "editando": "yellow",
            "sucesso": "green",
            "erro": "red",
            "padrao": "gray"
        }
        self.status_indicator.itemconfig(self.status_circle, fill=cores.get(estado, "gray"))

    def _validar_dados(self):
        erros = []
        data = self.entry_data.get()

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", data):
            erros.append("Formato de data inválido (DD/MM/AAAA)")
        else:
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                erros.append("Data inválida ou inexistente")

        tipo = self.var_tipo.get()
        if not tipo or tipo == "Digite para buscar...":
            erros.append("Tipo de atendimento obrigatório")
        elif tipo not in self.todos_tipos:
            erros.append("Selecione um tipo de atendimento válido da lista")

        descricao = self.txt_descricao.get("1.0", "end-1c").strip()
        if not descricao:
            erros.append("Descrição obrigatória")
        elif len(descricao) < 1:
            erros.append("Descrição muito curta (mínimo 1 caracteres)")

        return erros

    def _salvar(self):
        self.btn_salvar.config(state=tk.DISABLED, text="Salvando...")
        self._atualizar_status("editando")

        try:
            erros = self._validar_dados()
            if erros:
                raise ValueError("\n• " + "\n• ".join(erros))

            data_db = datetime.strptime(self.entry_data.get(), "%d/%m/%Y").strftime("%Y-%m-%d")

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
            # Novamente, simplifica a chamada e garante que a conexão é bem gerenciada.
            query = """
                INSERT INTO atividades (
                    colaborador_id, data_atendimento, tipo_atendimento_id,
                    nivel_complexidade, numero_atendimento, descricao,
                    status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, params=tuple(dados.values()), fetch=False)

            messagebox.showinfo("Sucesso", "Registro salvo com sucesso!", parent=self.master)
            self._limpar_formulario()
            self._atualizar_status("sucesso")

            self.btn_salvar.config(text="Salvo ✓")
            self.master.after(1200, lambda: self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)"))

        except ValueError as ve:
            self._atualizar_status("erro")
            messagebox.showerror("Erro de Validação", str(ve))
            self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")

        except Exception as e:
            self._atualizar_status("erro")
            logging.error(f"Erro ao salvar: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados.\n{str(e)}")
            self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")

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

    def _limpar_busca(self, event=None):
        self.combo_tipo.set('')
        self.combo_tipo['values'] = list(self.todos_tipos.keys())
        return "break"

    def _tipo_selecionado(self, event):
        if self.var_tipo.get() not in self.todos_tipos:
            self.var_tipo.set('')
        self._atualizar_status("editando")

    def _abrir_flutuante(self):
        try:
            dados = {
                'data': self.entry_data.get(),
                'tipo': self.var_tipo.get(),
                'nivel': self.var_nivel.get(),
                'ticket': self.entry_ticket.get().strip(),
                'descricao': self.txt_descricao.get("1.0", tk.END).strip(),
                'status': self.var_status.get() if hasattr(self, 'var_status') else None
            }

            root_window = self.master.winfo_toplevel()

            try:
                from screens.registro_atividade_flutuante_view import RegistroFlutuante
            except ImportError:
                try:
                    from registro_atividade_flutuante_view import RegistroFlutuante
                except ImportError as e:
                    messagebox.showerror("Erro", f"Não foi possível carregar a janela flutuante: {str(e)}",
                                         parent=root_window)
                    return

            self.flutuante = RegistroFlutuante(root_window, self.colaborador, dados)

            if not hasattr(self.flutuante, 'root') or not self.flutuante.root.winfo_exists():
                messagebox.showerror("Erro", "Falha ao criar a janela flutuante", parent=root_window)
                return

            self.flutuante.root.protocol("WM_DELETE_WINDOW", self._fechar_flutuante)

            root_window.withdraw()

            self.flutuante.root.focus_force()
            self.flutuante.root.lift()

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.master.winfo_toplevel().deiconify()
            messagebox.showerror("Erro", f"Falha ao abrir janela flutuante:\n{str(e)}", parent=self.master)

    def _fechar_flutuante(self):
        try:
            if hasattr(self, 'flutuante'):
                try:
                    if self.flutuante.root.winfo_exists():
                        self.flutuante.root.destroy()
                except tk.TclError:
                    pass
                del self.flutuante
        finally:
            root_window = self.master.winfo_toplevel()
            root_window.deiconify()
            root_window.focus_force()'''
# Versão FINAL com CORREÇÃO da Janela Flutuante
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from tkcalendar import Calendar
from utils.db import Database
import logging
import re


class RegistroAtividadeView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.db = Database()
        self.todos_tipos = {}
        self._after_id = None

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_tipos_atendimento()
        self._atualizar_painel_info()

        self.master.winfo_toplevel().bind("<Control-Return>", lambda e: self._salvar())

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", font=('Segoe UI', 10), background='#f8f9fa', foreground='#212929')
        style.configure("TFrame", background='#f8f9fa')
        style.configure("TLabel", background='#f8f9fa')
        style.configure("Title.TLabel", font=('Segoe UI', 18, "bold"))
        style.configure("DashboardTitle.TLabel", font=('Segoe UI', 14, "bold"), foreground="#007bff")
        style.configure("DashboardNumber.TLabel", font=('Segoe UI', 26, "bold"), foreground="#343a40")
        style.configure("DashboardSub.TLabel", font=('Segoe UI', 10), foreground="#6c757d")
        style.configure("Profile.TLabel", font=('Segoe UI', 10, 'bold'))
        style.configure("ProfileValue.TLabel", font=('Segoe UI', 10))
        style.configure("TLabelframe", background='#f8f9fa', bordercolor="#dee2e6")
        style.configure("TLabelframe.Label", background='#f8f9fa', foreground="#495057", font=('Segoe UI', 10, 'bold'))
        style.configure("TEntry", padding=5)
        style.configure("TCombobox", padding=5)
        style.configure("TButton", font=('Segoe UI', 10, 'bold'), padding=(10, 8), relief='flat', borderwidth=0)
        style.configure("Primary.TButton", background="#007bff", foreground="white")
        style.map("Primary.TButton", background=[('active', '#0056b3')])
        style.configure("Secondary.TButton", background="#6c757d", foreground="white")
        style.map("Secondary.TButton", background=[('active', '#5a6268')])
        style.configure("Info.TButton", background="#17a2b8", foreground="white")
        style.map("Info.TButton", background=[('active', '#117a8b')])
        style.configure("Calendar.TButton", background="#e9ecef", foreground="#495057", font=('Segoe UI', 9))
        style.map("Calendar.TButton", background=[('active', '#dce0e3')])

    def _setup_ui(self):
        self.master.columnconfigure(0, weight=2, uniform="group1")
        self.master.columnconfigure(1, weight=1, uniform="group1")
        self.master.rowconfigure(0, weight=1)
        form_frame = ttk.Frame(self.master, padding=(25, 20));
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10));
        form_frame.columnconfigure(1, weight=1)
        ttk.Label(form_frame, text="📄 Novo Registro de Atividade", style="Title.TLabel").grid(row=0, column=0,
                                                                                              columnspan=2,
                                                                                              pady=(0, 20), sticky='w')
        status_frame = ttk.Frame(form_frame);
        status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))
        self.status_indicator = tk.Canvas(status_frame, width=16, height=16, bg="#f8f9fa", highlightthickness=0);
        self.status_indicator.pack(side="left", padx=(0, 8))
        self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="gray", width=0)
        self.status_label = ttk.Label(status_frame, text="Preencha os campos para registrar");
        self.status_label.pack(side="left")
        campos = [("Data de Atendimento:", "entry_data"), ("Tipo de Atendimento:", "combo_tipo"),
                  ("Nível de Complexidade:", "combo_nivel"), ("Número/Ticket:", "entry_ticket"),
                  ("Status:", "combo_status"), ("Descrição:", "txt_descricao")]
        for i, (label_text, widget_name) in enumerate(campos):
            row = i + 2;
            ttk.Label(form_frame, text=label_text).grid(row=row, column=0, sticky="ne", pady=5, padx=(0, 10))
            if widget_name == "entry_data":
                frame = ttk.Frame(form_frame);
                frame.grid(row=row, column=1, sticky="ew")
                self.entry_data = ttk.Entry(frame, width=15);
                self.entry_data.insert(0, datetime.today().strftime("%d/%m/%Y"));
                self.entry_data.pack(side="left")
                ttk.Button(frame, text="🗓️", command=self._abrir_calendario, style="Calendar.TButton", width=3).pack(
                    side="left", padx=8)
            elif widget_name == "combo_tipo":
                self.var_tipo = tk.StringVar();
                self.combo_tipo = ttk.Combobox(form_frame, textvariable=self.var_tipo, state="normal")
                self.combo_tipo.grid(row=row, column=1, sticky="ew");
                self.combo_tipo.set("Digite para buscar...");
                self.combo_tipo.bind('<KeyRelease>', self._filtrar_tipos_debounce);
                self.combo_tipo.bind('<FocusIn>', self._on_combo_focus);
                self.combo_tipo.bind('<<ComboboxSelected>>', lambda e: self._atualizar_status("editando"));
                self.combo_tipo.bind('<Escape>', self._limpar_busca)
            elif widget_name == "combo_nivel":
                self.var_nivel = tk.StringVar();
                self.combo_nivel = ttk.Combobox(form_frame, textvariable=self.var_nivel,
                                                values=["BAIXO", "MEDIO", "GRAVE", "GRAVISSIMO"], state="readonly")
                self.combo_nivel.grid(row=row, column=1, sticky="ew");
                self.combo_nivel.current(0)
            elif widget_name == "entry_ticket":
                self.entry_ticket = ttk.Entry(form_frame);
                self.entry_ticket.grid(row=row, column=1, sticky="ew")
            elif widget_name == "combo_status":
                self.var_status = tk.StringVar(value="RESOLVIDO");
                self.combo_status = ttk.Combobox(form_frame, textvariable=self.var_status,
                                                 values=["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"],
                                                 state="readonly")
                self.combo_status.grid(row=row, column=1, sticky="ew")
            elif widget_name == "txt_descricao":
                self.txt_descricao = tk.Text(form_frame, height=5, width=40, wrap="word", font=("Segoe UI", 10),
                                             relief="solid", borderwidth=1, highlightthickness=1,
                                             highlightcolor="#ced4da")
                self.txt_descricao.grid(row=row, column=1, sticky="ew", pady=(5, 10));
                self.txt_descricao.bind("<KeyPress>", lambda e: self._atualizar_status("editando"))
        btn_frame = ttk.Frame(form_frame);
        btn_frame.grid(row=len(campos) + 2, column=1, sticky="e", pady=20)
        ttk.Button(btn_frame, text="Flutuante", command=self._abrir_flutuante, style="Info.TButton").pack(side="left",
                                                                                                          padx=10)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar_formulario, style="Secondary.TButton").pack(
            side="left", padx=10)
        self.btn_salvar = ttk.Button(btn_frame, text="Salvar (Ctrl+Enter)", command=self._salvar,
                                     style="Primary.TButton");
        self.btn_salvar.pack(side="left")
        profile_card = ttk.LabelFrame(form_frame, text="Colaborador");
        profile_card.grid(row=len(campos) + 3, column=0, columnspan=2, sticky='ew', pady=(10, 0));
        profile_card.columnconfigure(1, weight=1)
        self.nome_var = tk.StringVar();
        self.setor_var = tk.StringVar();
        self.cargo_var = tk.StringVar()
        ttk.Label(profile_card, text="Nome:", style="Profile.TLabel").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(profile_card, textvariable=self.nome_var, style="ProfileValue.TLabel", wraplength=350).grid(row=0,
                                                                                                              column=1,
                                                                                                              sticky='w',
                                                                                                              padx=5,
                                                                                                              pady=2)
        ttk.Label(profile_card, text="Setor:", style="Profile.TLabel").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(profile_card, textvariable=self.setor_var, style="ProfileValue.TLabel").grid(row=1, column=1,
                                                                                               sticky='w', padx=5,
                                                                                               pady=2)
        ttk.Label(profile_card, text="Cargo:", style="Profile.TLabel").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(profile_card, textvariable=self.cargo_var, style="ProfileValue.TLabel").grid(row=2, column=1,
                                                                                               sticky='w', padx=5,
                                                                                               pady=2)
        info_panel = ttk.Frame(self.master, padding=(20, 25));
        info_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ttk.Label(info_panel, text="Seu Desempenho", style="DashboardTitle.TLabel").pack(anchor='w')
        ttk.Separator(info_panel, orient='horizontal').pack(fill='x', pady=(5, 20), anchor='n')
        self.hoje_var = tk.StringVar(value="...");
        hoje_frame = ttk.Frame(info_panel);
        hoje_frame.pack(pady=10, anchor='center')
        ttk.Label(hoje_frame, textvariable=self.hoje_var, style="DashboardNumber.TLabel").pack()
        ttk.Label(hoje_frame, text="Registros Hoje", style="DashboardSub.TLabel").pack()
        self.semana_var = tk.StringVar(value="...");
        semana_frame = ttk.Frame(info_panel);
        semana_frame.pack(pady=10, anchor='center')
        ttk.Label(semana_frame, textvariable=self.semana_var, style="DashboardNumber.TLabel").pack()
        ttk.Label(semana_frame, text="Nesta Semana", style="DashboardSub.TLabel").pack()
        self.mes_var = tk.StringVar(value="...");
        mes_frame = ttk.Frame(info_panel);
        mes_frame.pack(pady=10, anchor='center')
        ttk.Label(mes_frame, textvariable=self.mes_var, style="DashboardNumber.TLabel").pack()
        ttk.Label(mes_frame, text="Neste Mês", style="DashboardSub.TLabel").pack()

    def _atualizar_painel_info(self):
        try:
            hoje = date.today().isoformat()
            query_hoje = "SELECT COUNT(id) as total FROM atividades WHERE colaborador_id = %s AND DATE(data_atendimento) = %s"
            res_hoje = self.db.execute_query(query_hoje, (self.colaborador.id, hoje))
            self.hoje_var.set(str(res_hoje[0]['total'] if res_hoje else 0))
            query_semana = "SELECT COUNT(id) as total FROM atividades WHERE colaborador_id = %s AND YEARWEEK(data_atendimento, 1) = YEARWEEK(CURDATE(), 1)"
            res_semana = self.db.execute_query(query_semana, (self.colaborador.id,))
            self.semana_var.set(str(res_semana[0]['total'] if res_semana else 0))
            query_mes = "SELECT COUNT(id) as total FROM atividades WHERE colaborador_id = %s AND YEAR(data_atendimento) = YEAR(CURDATE()) AND MONTH(data_atendimento) = MONTH(CURDATE())"
            res_mes = self.db.execute_query(query_mes, (self.colaborador.id,))
            self.mes_var.set(str(res_mes[0]['total'] if res_mes else 0))
            query_setor = "SELECT nome_setor FROM setores WHERE id = %s"
            res_setor = self.db.execute_query(query_setor, (self.colaborador.setor_id,))
            nome_setor = res_setor[0]['nome_setor'] if res_setor else "Não definido"
            self.nome_var.set(self.colaborador.nome);
            self.setor_var.set(nome_setor);
            self.cargo_var.set(self.colaborador.cargo.name.replace("_", " ").title())
        except Exception as e:
            logging.error(f"Erro ao atualizar painel: {e}", exc_info=True)
            self.hoje_var.set("N/A");
            self.semana_var.set("N/A");
            self.mes_var.set("N/A")
            self.nome_var.set("N/A");
            self.setor_var.set("N/A");
            self.cargo_var.set("N/A")

    def _salvar(self):
        self.btn_salvar.configure(state=tk.DISABLED, text="Salvando...")
        self.master.update_idletasks()
        try:
            erros = self._validar_dados()
            if erros: raise ValueError("\n• " + "\n• ".join(erros))
            data_db = datetime.strptime(self.entry_data.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            dados = {"colaborador_id": self.colaborador.id, "data_atendimento": data_db,
                     "tipo_atendimento_id": self.todos_tipos[self.var_tipo.get()],
                     "nivel_complexidade": self.var_nivel.get(),
                     "numero_atendimento": self.entry_ticket.get().strip() or None,
                     "descricao": self.txt_descricao.get("1.0", "end-1c").strip(), "status": self.var_status.get()}
            query = "INSERT INTO atividades (colaborador_id, data_atendimento, tipo_atendimento_id, nivel_complexidade, numero_atendimento, descricao, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.db.execute_query(query, params=tuple(dados.values()), fetch=False)
            self._atualizar_status("sucesso", "Registro salvo com sucesso!")
            self._limpar_formulario()
            self._atualizar_painel_info()
        except ValueError as ve:
            self._atualizar_status("erro", str(ve))
        except Exception as e:
            self._atualizar_status("erro", "Falha ao salvar no banco.");
            logging.error(f"Erro ao salvar: {e}", exc_info=True);
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados.\n{e}")
        finally:
            self.btn_salvar.configure(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")

    def _carregar_tipos_atendimento(self):
        try:
            tipos = self.db.execute_query("SELECT id, nome FROM tipos_atendimento ORDER BY nome")
            self.todos_tipos = {row['nome']: row['id'] for row in tipos} if tipos else {}
            self.combo_tipo['values'] = list(self.todos_tipos.keys())
        except Exception as e:
            logging.error(f"Erro ao carregar tipos: {e}", exc_info=True);
            messagebox.showerror("Erro de Conexão", "Não foi possível carregar os tipos de atendimento.")
            self.todos_tipos = {};
            self.combo_tipo['values'] = []

    def _atualizar_status(self, estado, mensagem=None):
        cores = {"editando": "#ffc107", "sucesso": "#28a745", "erro": "#dc3545", "padrao": "gray"}
        mensagens = {"editando": "Editando...", "sucesso": "Salvo!", "erro": "Erro de validação",
                     "padrao": "Preencha os campos para registrar"}
        self.status_indicator.itemconfig(self.status_circle, fill=cores.get(estado, "gray"))
        self.status_label.config(text=mensagem if mensagem else mensagens.get(estado, ""))

    def _validar_dados(self):
        erros = []
        try:
            datetime.strptime(self.entry_data.get(), "%d/%m/%Y")
        except ValueError:
            erros.append("Data inválida (use DD/MM/AAAA)")
        if (tipo := self.var_tipo.get()) not in self.todos_tipos: erros.append(
            "Tipo de atendimento inválido" if tipo and tipo != "Digite para buscar..." else "Tipo de atendimento obrigatório")
        if not self.txt_descricao.get("1.0", "end-1c").strip(): erros.append("Descrição obrigatória")
        return erros

    def _limpar_formulario(self):
        self.entry_data.delete(0, tk.END);
        self.entry_data.insert(0, datetime.today().strftime('%d/%m/%Y'))
        self.combo_tipo.set('Digite para buscar...');
        self.combo_nivel.current(0);
        self.entry_ticket.delete(0, tk.END)
        self.txt_descricao.delete("1.0", tk.END);
        self.var_status.set("RESOLVIDO");
        self._atualizar_status("padrao");
        self.combo_tipo.focus()

    def _on_combo_focus(self, event=None):
        if self.combo_tipo.get() == "Digite para buscar...": self.combo_tipo.set('')
        self.combo_tipo['values'] = list(self.todos_tipos.keys())

    def _filtrar_tipos_debounce(self, event):
        if event.keysym in ('Return', 'Up', 'Down', 'Left', 'Right', 'Escape', 'Tab'): return
        if self._after_id: self.master.after_cancel(self._after_id)
        self._after_id = self.master.after(300, self._executar_filtro)

    def _executar_filtro(self):
        self._after_id = None;
        texto = self.combo_tipo.get()
        if not texto or texto == "Digite para buscar...": self.combo_tipo['values'] = list(
            self.todos_tipos.keys()); return
        texto_lower = texto.lower();
        valores_filtrados = [item for item in self.todos_tipos.keys() if texto_lower in item.lower()]
        posicao_cursor = self.combo_tipo.index(tk.INSERT)
        self.combo_tipo['values'] = valores_filtrados if valores_filtrados else list(self.todos_tipos.keys())
        self.combo_tipo.set(texto);
        self.combo_tipo.icursor(posicao_cursor)
        if valores_filtrados: self.combo_tipo.event_generate('<Down>')

    def _abrir_calendario(self):
        top = tk.Toplevel(self.master);
        top.title("Selecione a Data");
        top.resizable(False, False);
        top.transient(self.master);
        top.grab_set()
        cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy", locale='pt_BR');
        cal.pack(pady=10, padx=10)

        def set_date(): self.entry_data.delete(0, tk.END); self.entry_data.insert(0,
                                                                                  cal.get_date()); top.destroy(); self._atualizar_status(
            "editando")

        ttk.Button(top, text="Selecionar", command=set_date, style="Primary.TButton").pack(pady=5)

    def _limpar_busca(self, event=None):
        self.combo_tipo.set('');
        self.combo_tipo['values'] = list(self.todos_tipos.keys());
        return "break"

    def _abrir_flutuante(self):
        try:
            dados = {'data': self.entry_data.get(), 'tipo': self.var_tipo.get(), 'nivel': self.var_nivel.get(),
                     'ticket': self.entry_ticket.get().strip(),
                     'descricao': self.txt_descricao.get("1.0", tk.END).strip(), 'status': self.var_status.get()}

            # <<< CORREÇÃO: A janela principal é a `Toplevel` da HomeView, não o frame de conteúdo >>>
            root_window = self.master.winfo_toplevel()

            from screens.registro_atividade_flutuante_view import RegistroFlutuante

            # Passa a janela principal correta como 'master' para a nova janela
            self.flutuante = RegistroFlutuante(root_window, self.colaborador, dados)
            self.flutuante.root.protocol("WM_DELETE_WINDOW", self._fechar_flutuante)

            # <<< CORREÇÃO: Removendo o withdraw() que causava o problema >>>
            # root_window.withdraw()

            self.flutuante.root.focus_force()
        except ImportError:
            messagebox.showerror("Erro", "Não foi possível carregar a janela flutuante.", parent=self.master)
        except Exception as e:
            import traceback;
            traceback.print_exc()
            messagebox.showerror("Erro", f"Falha ao abrir janela flutuante:\n{e}", parent=self.master)

    def _fechar_flutuante(self):
        try:
            if hasattr(self, 'flutuante') and self.flutuante.root.winfo_exists():
                self.flutuante.root.destroy()
                del self.flutuante
        finally:
            # <<< CORREÇÃO: Não é mais necessário, pois a janela principal não foi escondida >>>
            # root_window = self.master.winfo_toplevel()
            # root_window.deiconify()
            # root_window.focus_force()
            pass