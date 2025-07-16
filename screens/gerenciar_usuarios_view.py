import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
from screens.editar_usuario_view import EditarUsuarioView

class GerenciarUsuariosView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))
        style.configure("Treeview", font=('Segoe UI', 10))
        style.configure("TButton", font=('Segoe UI', 10))
        style.configure("TLabel", font=('Segoe UI', 12))

        self.frame = ttk.Frame(master, padding=20)
        self.frame.pack(fill='both', expand=True)

        # Título
        ttk.Label(
            self.frame,
            text="👥 Gestão de Usuários",
            font=('Segoe UI', 18, 'bold')
        ).pack(anchor='center', pady=(0, 15))

        # Área de botão
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(
            button_frame,
            text="➕ Novo Usuário",
            command=self._novo_usuario
        ).pack(side='right')

        # Tabela de usuários
        self.tree = ttk.Treeview(
            self.frame,
            columns=('id', 'nome', 'email', 'usuario', 'cargo', 'setor', 'status'),
            show='headings',
            height=15
        )
        self.tree.pack(fill='both', expand=True)

        # Cabeçalhos e largura
        col_config = {
            'id': 60,
            'nome': 150,
            'email': 180,
            'usuario': 120,
            'cargo': 120,
            'setor': 120,
            'status': 80
        }

        for col, width in col_config.items():
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor='center', width=width)

        self.tree.bind("<Double-1>", self._abrir_edicao)
        self._carregar_colaboradores()

    def _carregar_colaboradores(self):
        try:
            cursor = Database().get_cursor()
            query = """
                SELECT c.id, c.nome, c.email, c.usuario, c.cargo,
                       s.nome_setor AS setor, c.status
                FROM colaboradores c
                JOIN setores s ON c.setor_id = s.id
                ORDER BY c.nome
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())

            for row in resultados:
                self.tree.insert('', 'end', iid=row['id'], values=(
                    row['id'], row['nome'], row['email'], row['usuario'],
                    row['cargo'], row['setor'], row['status']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar usuários:\n{e}")

    def _abrir_edicao(self, event):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
            return

        usuario_id = int(selecionado)
        top = tk.Toplevel(self.master)
        EditarUsuarioView(top, usuario_id, on_save=self._carregar_colaboradores)

    def _novo_usuario(self):
        top = tk.Toplevel(self.master)
        EditarUsuarioView(top, usuario_id=None, on_save=self._carregar_colaboradores)
