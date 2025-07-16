import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from utils.db import Database
import logging

class EditarAtividadeView:
    def __init__(self, master, atividade_id, colaborador, on_save):
        self.master = master
        self.atividade_id = atividade_id
        self.colaborador = colaborador
        self.on_save = on_save
        self.db = Database()
        self.tipos_atendimento = {}

        self._configurar_estilos()
        self._carregar_tipos()
        self._carregar_dados()
        self._setup_ui()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#f8f9fa", font=("Segoe UI", 14, "bold"))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TCombobox", font=("Segoe UI", 10))
        style.configure("Primary.TButton", background="#4a6da7", foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Primary.TButton", background=[("active", "#3a5a8a")])

    def _carregar_tipos(self):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT id, nome FROM tipos_atendimento ORDER BY nome")
            self.tipos_atendimento = {row["nome"]: row["id"] for row in cursor.fetchall()}
        except Exception as e:
            logging.error("Erro ao carregar tipos de atendimento", exc_info=True)

    def _carregar_dados(self):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM atividades WHERE id = %s", (self.atividade_id,))
            self.dados = cursor.fetchone()
            if not self.dados:
                raise Exception("Atividade não encontrada")
        except Exception as e:
            logging.error("Erro ao carregar dados da atividade", exc_info=True)
            messagebox.showerror("Erro", "Erro ao carregar os dados da atividade.")
            self.master.destroy()

    def _setup_ui(self):
        self.master.geometry("420x420")
        self.master.configure(bg="#f8f9fa")

        frame = ttk.Frame(self.master, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Editar Atividade", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 10))

        # Data
        ttk.Label(frame, text="Data do Atendimento:").grid(row=1, column=0, sticky="w")
        self.entry_data = DateEntry(frame, date_pattern='dd-mm-yyyy')
        self.entry_data.grid(row=1, column=1, pady=5, sticky='we')
        self.entry_data.set_date(self.dados["data_atendimento"])

        # Tipo
        ttk.Label(frame, text="Tipo de Atendimento:").grid(row=2, column=0, sticky="w")
        self.var_tipo = tk.StringVar()
        self.combo_tipo = ttk.Combobox(frame, textvariable=self.var_tipo,
                                       values=list(self.tipos_atendimento.keys()), state="readonly")
        self.combo_tipo.grid(row=2, column=1, pady=5, sticky='we')
        for nome, id_ in self.tipos_atendimento.items():
            if id_ == self.dados["tipo_atendimento_id"]:
                self.var_tipo.set(nome)
                break

        # Nível
        ttk.Label(frame, text="Nível de Complexidade:").grid(row=3, column=0, sticky="w")
        self.var_nivel = tk.StringVar()
        self.combo_nivel = ttk.Combobox(frame, textvariable=self.var_nivel,
                                        values=["baixo", "medio", "grave", "gravissimo"], state="readonly")
        self.combo_nivel.grid(row=3, column=1, pady=5, sticky='we')
        self.var_nivel.set(self.dados["nivel_complexidade"])

        # Número
        ttk.Label(frame, text="Número/Ticket:").grid(row=4, column=0, sticky="w")
        self.entry_ticket = ttk.Entry(frame)
        self.entry_ticket.grid(row=4, column=1, pady=5, sticky='we')
        self.entry_ticket.insert(0, self.dados["numero_atendimento"] or "")

        # Descrição
        ttk.Label(frame, text="Descrição:").grid(row=5, column=0, sticky="nw")
        self.txt_descricao = tk.Text(frame, height=5, wrap='word')
        self.txt_descricao.grid(row=5, column=1, pady=5, sticky='we')
        self.txt_descricao.insert("1.0", self.dados["descricao"])

        # Botão salvar
        ttk.Button(frame, text="Salvar Alterações", command=self._salvar,
                   style="Primary.TButton").grid(row=6, column=0, columnspan=2, pady=15)

        frame.columnconfigure(1, weight=1)

    def _salvar(self):
        try:
            nova_data = self.entry_data.get_date().strftime('%Y-%m-%d')
            tipo_id = self.tipos_atendimento[self.var_tipo.get()]
            nivel = self.var_nivel.get()
            numero = self.entry_ticket.get().strip()
            descricao = self.txt_descricao.get("1.0", tk.END).strip()

            cursor = self.db.get_cursor()
            cursor.execute("""
                UPDATE atividades
                SET data_atendimento = %s,
                    tipo_atendimento_id = %s,
                    nivel_complexidade = %s,
                    numero_atendimento = %s,
                    descricao = %s
                WHERE id = %s
            """, (nova_data, tipo_id, nivel, numero or None, descricao, self.atividade_id))
            self.db.conn.commit()

            messagebox.showinfo("Sucesso", "Atividade atualizada com sucesso.")
            if self.on_save:
                self.on_save()
            self.master.destroy()

        except Exception as e:
            logging.error("Erro ao atualizar atividade", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao salvar alterações:\n{e}")