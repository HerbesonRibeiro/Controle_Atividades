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
        self.tipos_atendimento = {}

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_tipos_atendimento()
        self._configurar_atalhos()
        # self._centralizar_janela() #Apenas se for usar uma Janela

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

    def _centralizar_janela(self):
        self.master.update_idletasks()
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (w // 2)
        y = (self.master.winfo_screenheight() // 2) - (h // 2)
        self.master.geometry(f"{w}x{h}+{x}+{y}")

    def _configurar_atalhos(self):
        self.master.bind("<Control-Return>", lambda e: self._salvar())
        self.master.bind("<Escape>", lambda e: self.master.destroy())

    def _carregar_tipos_atendimento(self):
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("SELECT id, nome FROM tipos_atendimento ORDER BY nome")
                self.tipos_atendimento = {row["nome"]: row["id"] for row in cursor.fetchall() or []}
                if hasattr(self, "combo_tipo"):
                    self.combo_tipo["values"] = list(self.tipos_atendimento.keys())
                    if self.tipos_atendimento:
                        self.var_tipo.set(next(iter(self.tipos_atendimento)))
        except Exception as e:
            logging.error(f"Erro ao carregar tipos: {str(e)}", exc_info=True)
            messagebox.showwarning("Aviso", "Erro ao carregar tipos de atendimento.")

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

        ttk.Label(main_frame, text="Registro de Atividades", style="Title.TLabel").grid(
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
            ("Tipo de Atendimento:", "combo_tipo", list(self.tipos_atendimento.keys())),
            ("Nível de Complexidade:", "combo_nivel", ["baixo", "medio", "grave", "gravissimo"]),
            ("Número/Ticket:", "entry_ticket", ""),
            ("Descrição:", "txt_descricao", "")
        ]

        for row, (label, var_name, default) in enumerate(campos, start=2):
            ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="e", pady=4, padx=5)

            if "combo" in var_name:
                var = tk.StringVar()
                setattr(self, f"var_{var_name.split('_')[1]}", var)
                combo = ttk.Combobox(main_frame, textvariable=var, values=default, state="readonly")
                combo.grid(row=row, column=1, pady=4, sticky="we")
                setattr(self, var_name, combo)
                var.set(default[0] if default else "")

            elif var_name == "entry_data":
                frame = ttk.Frame(main_frame)
                frame.grid(row=row, column=1, sticky="we")
                entry = ttk.Entry(frame, width=15)
                entry.insert(0, default)
                entry.pack(side="left")
                setattr(self, var_name, entry)
                ttk.Button(frame, text="🗓️ Escolher", command=self._abrir_calendario,
                           style="Calendar.TButton").pack(side="left", padx=8)

            elif var_name == "entry_ticket":
                entry = ttk.Entry(main_frame)
                entry.grid(row=row, column=1, sticky="we")
                setattr(self, var_name, entry)

            elif var_name == "txt_descricao":
                text = tk.Text(main_frame, height=4, width=40, wrap="word")
                text.grid(row=row, column=1, pady=4, sticky="we")
                setattr(self, var_name, text)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=15)

        self.btn_salvar = ttk.Button(btn_frame, text="Salvar (Ctrl+Enter)",
                                     command=self._salvar, style="Primary.TButton")
        self.btn_salvar.pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Limpar", command=self._limpar_formulario).pack(side="left", padx=5)
        main_frame.columnconfigure(1, weight=1, minsize=250)

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
        if not re.match(r"\d{2}/\d{2}/\d{4}", data):
            erros.append("Data inválida (DD/MM/AAAA)")
        else:
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                erros.append("Data inválida")

        if not self.var_tipo.get():
            erros.append("Tipo de atendimento obrigatório")
        if not self.txt_descricao.get("1.0", "end-1c").strip():
            erros.append("Descrição obrigatória")

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
                "tipo_atendimento_id": self.tipos_atendimento[self.var_tipo.get()],
                "nivel_complexidade": self.var_nivel.get(),
                "numero_atendimento": self.entry_ticket.get().strip() or None,
                "descricao": self.txt_descricao.get("1.0", "end-1c").strip()
            }

            with self.db.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO atividades (
                        colaborador_id, data_atendimento, tipo_atendimento_id,
                        nivel_complexidade, numero_atendimento, descricao
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, tuple(dados.values()))
                self.db.conn.commit()

            messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")
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
            messagebox.showerror("Erro", "Erro ao salvar no banco de dados.")
            self.btn_salvar.config(state=tk.NORMAL, text="Salvar (Ctrl+Enter)")

    def _limpar_formulario(self):
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.today().strftime('%d/%m/%Y'))
        if self.tipos_atendimento:
            self.var_tipo.set(next(iter(self.tipos_atendimento)))
        self.var_nivel.set("baixo")
        self.entry_ticket.delete(0, tk.END)
        self.txt_descricao.delete("1.0", tk.END)
        self._atualizar_status("padrao")