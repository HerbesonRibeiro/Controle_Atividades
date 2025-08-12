# Versão FINAL e CORRIGIDA (de verdade)
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from utils.db import Database
import logging
from mysql.connector import Error


class EditarAtividadeView:
    # <<< CORREÇÃO FINAL: Adicionando o parâmetro 'colaborador' que faltava >>>
    def __init__(self, master, atividade_id, on_save, colaborador=None):
        self.master = master
        self.atividade_id = atividade_id
        self.on_save = on_save
        self.colaborador = colaborador  # Embora não usado aqui, é bom recebê-lo para evitar erros
        self.db = Database()
        self.tipos_atendimento = {}

        self.master.title("Editar Atividade")
        self.master.geometry("500x520")
        self.master.resizable(False, False)
        self.master.configure(bg="#f8f9fa")

        self._configurar_estilos()
        self._carregar_dados_iniciais()
        self._setup_ui()
        self._centralizar_janela()

    def _centralizar_janela(self):
        self.master.update_idletasks()
        x = (self.master.winfo_screenwidth() // 2) - (self.master.winfo_width() // 2)
        y = (self.master.winfo_screenheight() // 2) - (self.master.winfo_height() // 2)
        self.master.geometry(f'+{x}+{y}')

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f8f9fa")
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 16, "bold"))
        style.configure("TLabel", background="#f8f9fa")
        style.configure("TEntry", padding=5)
        style.configure("TCombobox")
        style.configure("Primary.TButton", background="#007bff", foreground="white", font=("Segoe UI", 10, "bold"),
                        padding=(12, 8))
        style.map("Primary.TButton", background=[("active", "#0056b3")])

    def _carregar_dados_iniciais(self):
        try:
            tipos_result = self.db.execute_query("SELECT id, nome FROM tipos_atendimento ORDER BY nome")
            self.tipos_atendimento = {row["nome"]: row["id"] for row in tipos_result}

            atividade_result = self.db.execute_query("SELECT * FROM atividades WHERE id = %s", (self.atividade_id,))
            if not atividade_result:
                raise Exception("Atividade não encontrada")
            self.dados = atividade_result[0]

        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Falha ao carregar dados iniciais:\n{e}",
                                 parent=self.master)
            self.master.destroy()

    def _setup_ui(self):
        main_frame = ttk.Frame(self.master, padding=(25, 20))
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="✏️ Editar Atividade", style="Title.TLabel").grid(row=0, column=0, columnspan=2,
                                                                                     pady=(0, 20), sticky='w')

        ttk.Label(main_frame, text="Data do Atendimento:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_data = DateEntry(main_frame, date_pattern='dd-mm-yyyy', font=("Segoe UI", 10))
        self.entry_data.grid(row=1, column=1, pady=5, sticky='we')
        self.entry_data.set_date(self.dados["data_atendimento"])

        ttk.Label(main_frame, text="Tipo de Atendimento:").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        self.var_tipo = tk.StringVar()
        self.combo_tipo = ttk.Combobox(main_frame, textvariable=self.var_tipo,
                                       values=list(self.tipos_atendimento.keys()), state="readonly", style="TCombobox")
        self.combo_tipo.grid(row=2, column=1, pady=5, sticky='we')
        tipo_nome_atual = next(
            (nome for nome, id_ in self.tipos_atendimento.items() if id_ == self.dados["tipo_atendimento_id"]), "")
        self.var_tipo.set(tipo_nome_atual)

        ttk.Label(main_frame, text="Nível de Complexidade:").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=5)
        self.var_nivel = tk.StringVar()
        self.combo_nivel = ttk.Combobox(main_frame, textvariable=self.var_nivel,
                                        values=["baixo", "medio", "grave", "gravissimo"], state="readonly",
                                        style="TCombobox")
        self.combo_nivel.grid(row=3, column=1, pady=5, sticky='we')
        self.var_nivel.set(self.dados["nivel_complexidade"])

        ttk.Label(main_frame, text="Número/Ticket:").grid(row=4, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_ticket = ttk.Entry(main_frame, style="TEntry")
        self.entry_ticket.grid(row=4, column=1, pady=5, sticky='we')
        self.entry_ticket.insert(0, self.dados["numero_atendimento"] or "")

        ttk.Label(main_frame, text="Descrição:").grid(row=5, column=0, sticky="nw", padx=(0, 10), pady=5)
        self.txt_descricao = tk.Text(main_frame, height=6, wrap='word', font=("Segoe UI", 10), relief='solid',
                                     borderwidth=1, highlightthickness=1, highlightcolor="#ced4da")
        self.txt_descricao.grid(row=5, column=1, pady=5, sticky='we')
        self.txt_descricao.insert("1.0", self.dados["descricao"])

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=1, pady=(20, 0), sticky='e')
        ttk.Button(btn_frame, text="Salvar Alterações", command=self._salvar, style="Primary.TButton").pack()

    def _salvar(self):
        try:
            nova_data = self.entry_data.get_date().strftime('%Y-%m-%d')
            tipo_id = self.tipos_atendimento[self.var_tipo.get()]
            nivel = self.var_nivel.get()
            numero = self.entry_ticket.get().strip()
            descricao = self.txt_descricao.get("1.0", tk.END).strip()

            if not all([nova_data, tipo_id, nivel, descricao]):
                raise ValueError("Todos os campos, exceto Número/Ticket, são obrigatórios.")

            query = "UPDATE atividades SET data_atendimento = %s, tipo_atendimento_id = %s, nivel_complexidade = %s, numero_atendimento = %s, descricao = %s WHERE id = %s"
            params = (nova_data, tipo_id, nivel, numero or None, descricao, self.atividade_id)
            self.db.execute_query(query, params, fetch=False)
            messagebox.showinfo("Sucesso", "Atividade atualizada com sucesso.", parent=self.master)
            if self.on_save: self.on_save()
            self.master.destroy()
        except ValueError as ve:
            messagebox.showwarning("Aviso", str(ve), parent=self.master)
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Falha ao salvar alterações:\n{e}", parent=self.master)