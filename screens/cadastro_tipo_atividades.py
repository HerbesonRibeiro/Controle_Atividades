# Versão com ajuste fino no botão Salvar do pop-up
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils.db import Database
import logging
from mysql.connector import Error


class CadastroAtividadesView:
    def __init__(self, master):
        self.master = master
        self.db = Database()

        for widget in self.master.winfo_children():
            widget.destroy()

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_tipos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#f8f9fa")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 18, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=(10, 5), background='#e9ecef',
                        relief='flat')
        style.map("Treeview", background=[('selected', '#b8d8ff')])

        style.configure("Primary.TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=(12, 8),
                        background="#007bff",
                        foreground="white")
        style.map("Primary.TButton",
                  background=[("active", "#0056b3")])

        style.configure("Secondary.TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=(12, 8),
                        background="#6c757d",
                        foreground="white")
        style.map("Secondary.TButton",
                  background=[("active", "#5a6268")])

    def _setup_ui(self):
        frame = ttk.Frame(self.master, padding=(25, 20))
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="📝 Gerenciar Tipos de Atividade", style="Title.TLabel").pack(side='top', anchor='w',
                                                                                           pady=(0, 20))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(side='top', fill='x', pady=(0, 15))

        btn_novo = ttk.Button(btn_frame, text="Novo Tipo", command=self._abrir_novo_tipo, style="Primary.TButton")
        btn_novo.pack(side='right')

        btn_editar = ttk.Button(btn_frame, text="Editar Tipo", command=self._abrir_editar_tipo,
                                style="Secondary.TButton")
        btn_editar.pack(side='right', padx=(0, 10))

        tabela_frame = ttk.Frame(frame)
        tabela_frame.pack(side='top', fill='both', expand=True)
        tabela_frame.columnconfigure(0, weight=1)
        tabela_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tabela_frame, columns=("id", "nome"), show="headings", height=10)
        self.tree.heading("id", text="ID", anchor='w')
        self.tree.heading("nome", text="NOME DO TIPO DE ATIVIDADE", anchor='w')
        self.tree.column("id", width=80, stretch=False, anchor='w')
        self.tree.column("nome", width=400, stretch=True, anchor='w')

        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree.bind("<Double-1>", lambda event: self._abrir_editar_tipo())

    def _carregar_tipos(self):
        try:
            query = "SELECT id, nome FROM tipos_atendimento ORDER BY nome ASC"
            tipos = self.db.execute_query(query)

            self.tree.delete(*self.tree.get_children())
            if not tipos: return

            for row in tipos:
                self.tree.insert("", "end", values=(row["id"], row["nome"].upper()))
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao carregar tipos de atividade: {e}",
                                 parent=self.master)

    def _abrir_novo_tipo(self):
        self._abrir_janela_tipo()

    def _abrir_editar_tipo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um tipo de atividade para editar.", parent=self.master)
            return

        item = self.tree.item(selected[0])
        tipo_id, nome = item['values']
        self._abrir_janela_tipo(tipo_id, nome)

    def _abrir_janela_tipo(self, tipo_id=None, nome=""):
        janela = tk.Toplevel(self.master)
        janela.title("Editar Tipo de Atividade" if tipo_id else "Novo Tipo de Atividade")
        janela.configure(bg="#f8f9fa")
        janela.transient(self.master)
        janela.grab_set()

        janela.update_idletasks()
        width, height = 400, 180
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        janela.geometry(f'{width}x{height}+{x}+{y}')
        janela.resizable(False, False)

        container = ttk.Frame(janela, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Nome do Tipo de Atividade:").pack(anchor="w", pady=(0, 5))

        entry_nome = ttk.Entry(container, font=("Segoe UI", 10), width=50)
        entry_nome.pack(fill="x", ipady=5, pady=5)
        entry_nome.insert(0, nome)
        entry_nome.focus()

        def salvar():
            novo_nome = entry_nome.get().strip()
            if not novo_nome:
                messagebox.showwarning("Campo obrigatório", "Informe o nome.", parent=janela)
                return

            try:
                if tipo_id:
                    query = "UPDATE tipos_atendimento SET nome=%s WHERE id=%s"
                    params = (novo_nome, tipo_id)
                else:
                    query = "INSERT INTO tipos_atendimento (nome) VALUES (%s)"
                    params = (novo_nome,)

                self.db.execute_query(query, params, fetch=False)

                self._carregar_tipos()
                janela.destroy()
            except Error as e:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao salvar: {e}", parent=janela)

        # <<< DETALHE: Ajuste fino no texto e no 'pack' do botão Salvar >>>
        btn_salvar = ttk.Button(container, text="SALVAR", command=salvar, style="Primary.TButton")
        btn_salvar.pack(pady=15)  # Removido o ipadx
