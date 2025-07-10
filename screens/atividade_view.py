import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.atividade_controllers import AtendimentoController


class AtendimentoView(tk.Toplevel):
    def __init__(self, parent, colaborador):
        super().__init__(parent)
        self.title("Registrar Atendimento")
        self.geometry("600x500")
        self.resizable(False, False)

        self.colaborador = colaborador
        self.controller = AtendimentoController()
        self._setup_ui()

    def _setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        # Formulário
        tk.Label(main_frame, text="COLABORADOR:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky='w', pady=5)
        tk.Label(main_frame, text=self.colaborador, font=('Arial', 10)).grid(
            row=0, column=1, sticky='w', pady=5)

        tk.Label(main_frame, text="DIA DO ATENDIMENTO:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky='w', pady=5)
        self.data_entry = ttk.Entry(main_frame)
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.data_entry.grid(row=1, column=1, sticky='ew', pady=5)

        tk.Label(main_frame, text="TIPO DE ATENDIMENTO:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky='w', pady=5)
        self.tipo_combo = ttk.Combobox(
            main_frame,
            values=self.controller.obter_tipos_atendimento(),
            state='readonly'
        )
        self.tipo_combo.grid(row=2, column=1, sticky='ew', pady=5)

        tk.Label(main_frame, text="NÍVEL:", font=('Arial', 10, 'bold')).grid(
            row=3, column=0, sticky='w', pady=5)
        self.nivel_combo = ttk.Combobox(
            main_frame,
            values=self.controller.obter_niveis(),
            state='readonly'
        )
        self.nivel_combo.grid(row=3, column=1, sticky='ew', pady=5)

        tk.Label(main_frame, text="NÚMERO/TICKET:", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, sticky='w', pady=5)
        self.ticket_entry = ttk.Entry(main_frame)
        self.ticket_entry.grid(row=4, column=1, sticky='ew', pady=5)

        tk.Label(main_frame, text="STATUS:", font=('Arial', 10, 'bold')).grid(
            row=5, column=0, sticky='w', pady=5)
        self.status_combo = ttk.Combobox(
            main_frame,
            values=self.controller.obter_status(),
            state='readonly'
        )
        self.status_combo.grid(row=5, column=1, sticky='ew', pady=5)

        tk.Label(main_frame, text="DESCRIÇÃO:", font=('Arial', 10, 'bold')).grid(
            row=6, column=0, sticky='nw', pady=5)
        self.descricao_text = tk.Text(main_frame, height=8)
        self.descricao_text.grid(row=6, column=1, sticky='ew', pady=5)

        # Botões
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=7, column=1, sticky='e', pady=15)

        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Salvar", command=self._salvar).pack(side='right')

    def _salvar(self):
        dados = {
            'colaborador': self.colaborador,
            'data': self.data_entry.get(),
            'tipo': self.tipo_combo.get(),
            'nivel': self.nivel_combo.get(),
            'numero_ticket': self.ticket_entry.get(),
            'status': self.status_combo.get(),
            'descricao': self.descricao_text.get("1.0", tk.END).strip()
        }

        # Validação simples
        if not all([dados['tipo'], dados['nivel'], dados['status']]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        if self.controller.registrar_atendimento(**dados):
            messagebox.showinfo("Sucesso", "Atendimento registrado com sucesso!")
            self.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível registrar o atendimento")