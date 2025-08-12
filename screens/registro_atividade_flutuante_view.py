# Versão FINAL com comportamento de janela independente
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
from tkcalendar import Calendar
from utils.db import Database


class RegistroFlutuante:
    def __init__(self, master, colaborador, dados_iniciais=None):
        try:
            self.root = tk.Toplevel(master)
            self.root.title("Registro Flutuante")
            self.root.minsize(450, 480)

            # A "mágica" para flutuar sobre TUDO
            self.root.attributes('-topmost', True)

            # <<< CORREÇÃO: Removendo o vínculo que fazia a janela principal restaurar >>>
            # self.root.transient(master)
            # self.root.grab_set()

            self.db = Database()
            self.colaborador = colaborador
            self.todos_tipos = {}
            self._after_id = None

            self._configurar_estilos()
            self._setup_ui()
            self._centralizar_janela()
            self._carregar_tipos_atendimento()

            if dados_iniciais:
                self._preencher_campos(dados_iniciais)

            self.root.bind("<Control-Return>", lambda e: self._salvar())
            self.root.bind("<Escape>", lambda e: self._fechar_janela())

        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro Crítico", f"Falha ao inicializar janela flutuante: {e}", parent=master)

    # O resto da classe permanece o mesmo, pois o design e a lógica já estão ótimos.
    # ... (cole aqui o resto dos métodos da sua classe RegistroFlutuante, eles não precisam de alteração)
    def _centralizar_janela(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _configurar_estilos(self):
        style = ttk.Style();
        style.theme_use('clam')
        style.configure(".", font=('Segoe UI', 10), background='#f8f9fa', foreground='#212529')
        style.configure("TFrame", background='#f8f9fa');
        style.configure("TLabel", background='#f8f9fa')
        style.configure("Title.TLabel", font=('Segoe UI', 16, "bold"))
        style.configure("TEntry", padding=5);
        style.configure("TCombobox", padding=5)
        style.configure("TButton", font=('Segoe UI', 10, 'bold'), padding=(10, 8), relief='flat', borderwidth=0)
        style.configure("Primary.TButton", background="#007bff", foreground="white")
        style.map("Primary.TButton", background=[('active', '#0056b3')])
        style.configure("Secondary.TButton", background="#6c757d", foreground="white")
        style.map("Secondary.TButton", background=[('active', '#5a6268')])
        style.configure("Calendar.TButton", background="#e9ecef", foreground="#495057", font=('Segoe UI', 9))
        style.map("Calendar.TButton", background=[('active', '#dce0e3')])

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20");
        main_frame.pack(fill="both", expand=True);
        main_frame.columnconfigure(1, weight=1)
        ttk.Label(main_frame, text="📄 Registro Rápido", style="Title.TLabel").grid(row=0, column=0, columnspan=2,
                                                                                   pady=(0, 20), sticky="w")
        status_frame = ttk.Frame(main_frame);
        status_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))
        self.status_indicator = tk.Canvas(status_frame, width=16, height=16, bg="#f8f9fa", highlightthickness=0);
        self.status_indicator.pack(side="left", padx=(0, 8))
        self.status_circle = self.status_indicator.create_oval(2, 2, 14, 14, fill="gray", width=0)
        self.status_label = ttk.Label(status_frame, text="Preencha os campos para registrar");
        self.status_label.pack(side="left")
        campos = [("Data:", "entry_data"), ("Tipo:", "combo_tipo"), ("Nível:", "combo_nivel"),
                  ("Ticket:", "entry_ticket"), ("Status:", "combo_status"), ("Descrição:", "txt_descricao")]
        for i, (label_text, widget_name) in enumerate(campos):
            row = i + 2;
            ttk.Label(main_frame, text=label_text).grid(row=row, column=0, sticky="ne", pady=5, padx=(0, 10))
            if widget_name == "entry_data":
                frame = ttk.Frame(main_frame);
                frame.grid(row=row, column=1, sticky="ew")
                self.entry_data = ttk.Entry(frame, width=15);
                self.entry_data.insert(0, datetime.today().strftime("%d/%m/%Y"));
                self.entry_data.pack(side="left")
                ttk.Button(frame, text="🗓️", command=self._abrir_calendario, style="Calendar.TButton", width=3).pack(
                    side="left", padx=8)
            elif widget_name == "combo_tipo":
                self.var_tipo = tk.StringVar();
                self.combo_tipo = ttk.Combobox(main_frame, textvariable=self.var_tipo, state="normal")
                self.combo_tipo.grid(row=row, column=1, sticky="ew");
                self.combo_tipo.set("Digite para buscar...");
                self.combo_tipo.bind('<KeyRelease>', self._filtrar_tipos_debounce);
                self.combo_tipo.bind('<FocusIn>', self._on_combo_focus);
                self.combo_tipo.bind('<<ComboboxSelected>>', lambda e: self._atualizar_status("editando"));
                self.combo_tipo.bind('<Escape>', self._limpar_busca)
            elif widget_name == "combo_nivel":
                self.var_nivel = tk.StringVar();
                self.combo_nivel = ttk.Combobox(main_frame, textvariable=self.var_nivel,
                                                values=["BAIXO", "MEDIO", "GRAVE", "GRAVISSIMO"], state="readonly")
                self.combo_nivel.grid(row=row, column=1, sticky="ew");
                self.combo_nivel.current(0)
            elif widget_name == "entry_ticket":
                self.entry_ticket = ttk.Entry(main_frame);
                self.entry_ticket.grid(row=row, column=1, sticky="ew")
            elif widget_name == "combo_status":
                self.var_status = tk.StringVar(value="RESOLVIDO");
                self.combo_status = ttk.Combobox(main_frame, textvariable=self.var_status,
                                                 values=["RESOLVIDO", "FECHADO", "ENCAMINHADO", "PENDENTE"],
                                                 state="readonly")
                self.combo_status.grid(row=row, column=1, sticky="ew")
            elif widget_name == "txt_descricao":
                self.txt_descricao = tk.Text(main_frame, height=4, width=30, wrap="word", font=("Segoe UI", 10),
                                             relief="solid", borderwidth=1, highlightthickness=1,
                                             highlightcolor="#ced4da")
                self.txt_descricao.grid(row=row, column=1, sticky="ew", pady=(5, 10));
                self.txt_descricao.bind("<KeyPress>", lambda e: self._atualizar_status("editando"))
        btn_frame = ttk.Frame(main_frame);
        btn_frame.grid(row=len(campos) + 2, column=1, sticky="e", pady=15)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar_formulario, style="Secondary.TButton").pack(
            side="left", padx=10)
        self.btn_salvar = ttk.Button(btn_frame, text="Salvar", command=self._salvar, style="Primary.TButton");
        self.btn_salvar.pack(side="left")

    def _preencher_campos(self, dados):
        self.entry_data.delete(0, tk.END);
        self.entry_data.insert(0, dados.get('data', ''))
        self.combo_tipo.set(dados.get('tipo', ''));
        self.combo_nivel.set(dados.get('nivel', 'BAIXO'))
        self.entry_ticket.delete(0, tk.END);
        self.entry_ticket.insert(0, dados.get('ticket', ''))
        self.txt_descricao.delete("1.0", tk.END);
        self.txt_descricao.insert("1.0", dados.get('descricao', '').strip())
        if 'status' in dados and dados['status']: self.combo_status.set(dados['status'])

    def _salvar(self):
        self.btn_salvar.configure(state=tk.DISABLED, text="Salvando...")
        self.root.update_idletasks()
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
            self._atualizar_status("sucesso", "Registro salvo!")
            messagebox.showinfo("Sucesso", "Registro salvo com sucesso!", parent=self.root)
            self._limpar_formulario()
        except ValueError as ve:
            self._atualizar_status("erro", str(ve))
        except Exception as e:
            self._atualizar_status("erro", "Falha ao salvar.");
            logging.error(f"Erro ao salvar: {e}", exc_info=True);
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados.\n{e}", parent=self.root)
        finally:
            self.btn_salvar.configure(state=tk.NORMAL, text="Salvar")

    def _carregar_tipos_atendimento(self):
        try:
            tipos = self.db.execute_query("SELECT id, nome FROM tipos_atendimento ORDER BY nome")
            self.todos_tipos = {row['nome']: row['id'] for row in tipos} if tipos else {}
            self.combo_tipo['values'] = list(self.todos_tipos.keys())
        except Exception as e:
            logging.error(f"Erro ao carregar tipos: {e}", exc_info=True);
            messagebox.showerror("Erro de Conexão", "Não foi possível carregar os tipos de atendimento.",
                                 parent=self.root)
            self.todos_tipos = {};
            self.combo_tipo['values'] = []

    def _atualizar_status(self, estado, mensagem=None):
        cores = {"editando": "#ffc107", "sucesso": "#28a745", "erro": "#dc3545", "padrao": "gray"}
        mensagens = {"editando": "Editando...", "sucesso": "Salvo!", "erro": "Erro de validação",
                     "padrao": "Preencha os campos para registrar"}
        self.status_indicator.itemconfig(self.status_circle, fill=cores.get(estado, "gray"))
        self.status_label.config(text=mensagem if mensagem else mensagens.get(estado, ""))

    def _validar_dados(self):
        erros = [];
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
        if self._after_id: self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(300, self._executar_filtro)

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
        top = tk.Toplevel(self.root);
        top.title("Selecione a Data");
        top.resizable(False, False);
        top.transient(self.root);
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

    def _fechar_janela(self):
        self.root.destroy()