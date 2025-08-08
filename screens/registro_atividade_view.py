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
import tkinter as tk
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
            root_window.focus_force()
