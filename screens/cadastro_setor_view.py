# Versão FINAL com Tabela e Botões Proporcionais
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils.db import Database
import logging
from mysql.connector import Error


class CadastroSetorView:
    def __init__(self, master):
        self.master = master
        self.db = Database()

        for widget in self.master.winfo_children():
            widget.destroy()

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_setores()

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
        self.frame = ttk.Frame(self.master, padding=(25, 20))
        self.frame.pack(fill='both', expand=True)

        ttk.Label(self.frame, text="🏢 Gerenciar Setores", style="Title.TLabel").pack(side='top', anchor='w',
                                                                                     pady=(0, 20))

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(side='top', fill='x', pady=(0, 15))

        btn_novo = ttk.Button(btn_frame, text="Novo Setor", command=self._adicionar_setor, style="Primary.TButton")
        btn_novo.pack(side='right')

        btn_editar = ttk.Button(btn_frame, text="Editar Setor", command=self._editar_setor, style="Secondary.TButton")
        btn_editar.pack(side='right', padx=(0, 10))

        tabela_frame = ttk.Frame(self.frame)

        # <<< CORREÇÃO FINAL DA TABELA >>>
        # fill='x' -> Ocupa a largura disponível.
        # expand=False -> NÃO ocupa a altura disponível.
        tabela_frame.pack(side='top', fill='x', expand=False)

        tabela_frame.columnconfigure(0, weight=1)
        tabela_frame.rowconfigure(0, weight=1)

        self._criar_tabela(tabela_frame)

    def _criar_tabela(self, parent_frame):
        # <<< CORREÇÃO FINAL DA TABELA >>>
        # Adicionando uma altura fixa de 10 linhas para a tabela.
        self.tree = ttk.Treeview(parent_frame, columns=('id', 'nome_setor'), show='headings', selectmode='browse',
                                 height=10)

        col_config = {'id': {'width': 80, 'text': 'ID', 'stretch': False},
                      'nome_setor': {'width': 400, 'text': 'NOME DO SETOR', 'stretch': True}}
        for col, config in col_config.items():
            self.tree.heading(col, text=config['text'], anchor='w')
            self.tree.column(col, width=config['width'], anchor='w', stretch=config['stretch'])

        scrollbar = ttk.Scrollbar(parent_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree.bind("<Double-1>", lambda event: self._editar_setor())

    def _carregar_setores(self):
        try:
            query = "SELECT id, nome_setor FROM setores ORDER BY nome_setor ASC"
            setores = self.db.execute_query(query)
            self.tree.delete(*self.tree.get_children())
            if not setores: return
            for setor in setores:
                self.tree.insert('', 'end', values=(setor['id'], setor['nome_setor'].upper()))
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível carregar os setores.\n{e}",
                                 parent=self.master)

    def _adicionar_setor(self):
        novo_nome = simpledialog.askstring("Novo Setor", "Informe o nome do novo setor:", parent=self.master)
        if not novo_nome or not novo_nome.strip(): return
        try:
            query = "INSERT INTO setores (nome_setor) VALUES (%s)"
            self.db.execute_query(query, (novo_nome.strip(),), fetch=False)
            messagebox.showinfo("Sucesso", "Setor adicionado com sucesso.", parent=self.master)
            self._carregar_setores()
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível adicionar o setor.\n{e}",
                                 parent=self.master)

    def _editar_setor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um setor na tabela para editar (ou dê um duplo clique).",
                                   parent=self.master)
            return
        item = self.tree.item(selected[0])
        setor_id, nome_atual = item['values']
        novo_nome = simpledialog.askstring("Editar Setor", f"Novo nome para o setor '{nome_atual}':",
                                           initialvalue=nome_atual, parent=self.master)
        if not novo_nome or not novo_nome.strip(): return
        try:
            query = "UPDATE setores SET nome_setor = %s WHERE id = %s"
            self.db.execute_query(query, (novo_nome.strip(), setor_id), fetch=False)
            messagebox.showinfo("Sucesso", "Setor atualizado com sucesso.", parent=self.master)
            self._carregar_setores()
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível atualizar o setor.\n{e}",
                                 parent=self.master)