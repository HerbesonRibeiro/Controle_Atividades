import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from utils.db import Database
import logging

class RegistroAtividadeView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador

        frame = tk.Frame(self.master, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        self.tipos_atendimento = {}
        self._carregar_tipos_atendimento()
        self._setup_ui()

        # Atalhos
        self.master.bind('<Control-Return>', lambda e: self._salvar())
        self.master.bind('<Return>', lambda e: self._salvar())

    def _carregar_tipos_atendimento(self):
        """Carrega os tipos da tabela tipos_atendimento (id + nome)"""
        try:
            cursor = Database().get_cursor()
            cursor.execute("SELECT id, nome FROM tipos_atendimento ORDER BY nome")
            rows = cursor.fetchall()
            self.tipos_atendimento = {row['nome']: row['id'] for row in rows}
        except Exception as e:
            logging.error(f"Erro ao carregar tipos de atendimento: {e}")
            self.tipos_atendimento = {}

    def _setup_ui(self):
        frame = tk.Frame(self.master, bg='#f8f9fa', padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Status visual (círculo)
        self.status_color = tk.Canvas(frame, width=20, height=20, bg='#f8f9fa', highlightthickness=0)
        self.status_color.grid(row=0, column=0, sticky='w')
        self.status_circle = self.status_color.create_oval(2, 2, 18, 18, fill='yellow')

        # Data
        tk.Label(frame, text="Data do Atendimento:", bg='#f8f9fa').grid(row=1, column=0, sticky='e')
        self.entry_data = tk.Entry(frame)
        self.entry_data.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.entry_data.grid(row=1, column=1, pady=5, sticky='we')

        # Tipo Atendimento
        tk.Label(frame, text="Tipo de Atendimento:", bg='#f8f9fa').grid(row=2, column=0, sticky='e')
        self.var_tipo = tk.StringVar()
        self.combo_tipo = ttk.Combobox(
            frame,
            textvariable=self.var_tipo,
            values=list(self.tipos_atendimento.keys()),
            state='readonly'
        )
        self.combo_tipo.grid(row=2, column=1, pady=5, sticky='we')
        if self.tipos_atendimento:
            self.var_tipo.set(next(iter(self.tipos_atendimento)))

        # Nível Complexidade
        tk.Label(frame, text="Nível de Complexidade:", bg='#f8f9fa').grid(row=3, column=0, sticky='e')
        self.var_nivel = tk.StringVar()
        self.combo_nivel = ttk.Combobox(
            frame,
            textvariable=self.var_nivel,
            values=["baixo", "medio", "grave", "gravissimo"],
            state='readonly'
        )
        self.combo_nivel.grid(row=3, column=1, pady=5, sticky='we')
        self.var_nivel.set("baixo")

        # Número/Ticket
        tk.Label(frame, text="Número/Ticket:", bg='#f8f9fa').grid(row=4, column=0, sticky='e')
        self.entry_ticket = tk.Entry(frame)
        self.entry_ticket.grid(row=4, column=1, pady=5, sticky='we')

        # Descrição
        tk.Label(frame, text="Descrição:", bg='#f8f9fa').grid(row=5, column=0, sticky='ne')
        self.txt_descricao = tk.Text(frame, height=5)
        self.txt_descricao.grid(row=5, column=1, pady=5, sticky='we')

        # Detectar alterações
        for widget in [self.entry_data, self.entry_ticket, self.txt_descricao, self.combo_tipo, self.combo_nivel]:
            widget.bind("<Key>", lambda e: self._set_status("yellow"))

        # Botão Salvar
        self.btn_salvar = tk.Button(frame, text="Salvar", command=self._salvar, bg='#28a745', fg='white')
        self.btn_salvar.grid(row=6, column=0, columnspan=2, pady=15)

        frame.columnconfigure(1, weight=1)

    def _set_status(self, color):
        self.status_color.itemconfig(self.status_circle, fill=color)

    def _salvar(self):
        try:
            self.btn_salvar.config(state=tk.DISABLED, bg='#ffc107')
            data = self.entry_data.get()
            tipo_nome = self.var_tipo.get()
            tipo_id = self.tipos_atendimento.get(tipo_nome)
            nivel = self.var_nivel.get()
            numero = self.entry_ticket.get().strip()
            descricao = self.txt_descricao.get("1.0", tk.END).strip()

            if not tipo_id or not nivel or not descricao:
                raise ValueError("Preencha todos os campos obrigatórios.")

            cursor = Database().get_cursor()
            cursor.execute("""
                INSERT INTO atividades (
                    colaborador_id, 
                    data_atendimento, 
                    tipo_atendimento_id, 
                    nivel_complexidade, 
                    numero_atendimento, 
                    descricao
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                self.colaborador.id,
                data,
                tipo_id,
                nivel,
                numero if numero else None,
                descricao
            ))
            Database().conn.commit()

            messagebox.showinfo("Sucesso", "Atividade registrada com sucesso!")
            self._limpar_formulario()
            self._set_status("green")

        except Exception as e:
            logging.error(f"Erro ao registrar atividade: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao registrar: {e}")
            self._set_status("red")

        finally:
            self.btn_salvar.config(state=tk.NORMAL, bg='#28a745')

    def _limpar_formulario(self):
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.var_tipo.set(next(iter(self.tipos_atendimento)) if self.tipos_atendimento else "")
        self.var_nivel.set("baixo")
        self.entry_ticket.delete(0, tk.END)
        self.txt_descricao.delete("1.0", tk.END)
