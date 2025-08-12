# Versão com a chamada unificada para Novo/Editar Usuário
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
from screens.editar_usuario_view import EditarUsuarioView # <<< MUDANÇA: Usamos a mesma view para novo e editar
import logging
from mysql.connector import Error

class GerenciarUsuariosView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.db = Database()

        for widget in self.master.winfo_children():
            widget.destroy()

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_colaboradores()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#f8f9fa")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 18, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=(10, 5), background='#e9ecef', relief='flat')
        style.map("Treeview", background=[('selected', '#b8d8ff')])
        style.configure("Primary.TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=(12, 8),
                        background="#007bff",
                        foreground="white")
        style.map("Primary.TButton",
                  background=[("active", "#0056b3")])

    def _setup_ui(self):
        self.frame = ttk.Frame(self.master, padding=(25, 20))
        self.frame.pack(fill="both", expand=True)
        ttk.Label(self.frame, text="👥 Gestão de Usuários", style="Title.TLabel").pack(side='top', anchor="w", pady=(0, 20))
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(side='top', fill="x", pady=(0, 15))
        ttk.Button(btn_frame, text="Novo Usuário", command=self._novo_usuario, style="Primary.TButton").pack(side="right")
        self._criar_tabela()

    def _criar_tabela(self):
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(side='top', fill="both", expand=True)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(table_frame,
            columns=('id', 'nome', 'email', 'usuario', 'cargo', 'setor', 'status'),
            show='headings',
            selectmode='browse'
        )
        col_config = {
            'id': {'width': 50, 'stretch': False},
            'nome': {'width': 200, 'stretch': True},
            'email': {'width': 200, 'stretch': True},
            'usuario': {'width': 120, 'stretch': False},
            'cargo': {'width': 120, 'stretch': False},
            'setor': {'width': 120, 'stretch': False},
            'status': {'width': 80, 'stretch': False}
        }
        for col, cfg in col_config.items():
            self.tree.heading(col, text=col.upper(), anchor='w')
            self.tree.column(col, anchor='w', **cfg)
        self.tree.tag_configure('evenrow', background="#f2f2f2")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.bind("<Double-1>", self._abrir_edicao)

    def _carregar_colaboradores(self):
        try:
            query = "SELECT c.id, c.nome, c.email, c.usuario, c.cargo, s.nome_setor AS setor, c.status FROM colaboradores c JOIN setores s ON c.setor_id = s.id ORDER BY c.nome"
            resultados = self.db.execute_query(query)
            self.tree.delete(*self.tree.get_children())
            if not resultados: return
            for i, row in enumerate(resultados):
                status = "Ativo" if row['status'] else "Inativo"
                tag = 'evenrow' if i % 2 == 0 else ''
                self.tree.insert('', 'end', iid=row['id'], values=(
                    row['id'], row['nome'], row['email'], row['usuario'],
                    row['cargo'], row['setor'], status
                ), tags=(tag,))
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Falha ao carregar usuários:\n{e}", parent=self.master)

    def _abrir_edicao(self, event=None):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.", parent=self.master)
            return
        usuario_id = int(selecionado)
        top = tk.Toplevel(self.master)
        top.transient(self.master)
        top.grab_set()
        EditarUsuarioView(top, usuario_id, on_save=self._carregar_colaboradores)

    def _novo_usuario(self):
        top = tk.Toplevel(self.master)
        top.transient(self.master)
        top.grab_set()
        # <<< MUDANÇA: Chamando a mesma tela de Edição, mas sem passar um ID >>>
        # A lógica interna da EditarUsuarioView já sabe que, sem ID, é um usuário novo.
        EditarUsuarioView(top, usuario_id=None, on_save=self._carregar_colaboradores)