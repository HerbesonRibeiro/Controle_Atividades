# Revisado conexão com BD
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
from screens.editar_usuario_view import EditarUsuarioView
import logging
from mysql.connector import Error


class GerenciarUsuariosView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_colaboradores()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo escuro
        style.configure("Dark.TFrame", background="#1f1f1f")
        style.configure("Light.TFrame", background="#f4f6f7")
        style.configure("Title.TLabel", background="#f4f6f7", foreground="#1f1f1f",
                        font=("Segoe UI", 18, "bold"))

        style.configure("Subtitle.TLabel", background="#1f1f1f", foreground="#e0e0e0",
                        font=("Segoe UI", 10, "bold"))
        style.configure("Table.TFrame", background="#f4f6f7")
        style.configure("Primary.TButton", background="#2b2b2b", foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Primary.TButton", background=[("active", "#3a3a3a")])
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=24,
                        fieldbackground="#ffffff", background="#ffffff")
        style.configure("Treeview.Heading", font=('Segoe UI', 10, "bold"))

    def _setup_ui(self):
        # Layout principal: menu à esquerda e conteúdo à direita
        self.container = ttk.Frame(self.master, style="Light.TFrame", padding=15)
        self.container.pack(fill="both", expand=True)

        ttk.Label(self.container, text="👥 Gestão de Usuários", style="Title.TLabel").pack(anchor="w", pady=(0, 15))

        btn_frame = ttk.Frame(self.container, style="Light.TFrame")
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="➕ Novo Usuário", command=self._novo_usuario, style="Primary.TButton").pack(side="right")

        self._criar_tabela()

    def _criar_tabela(self):
        table_frame = ttk.Frame(self.container, style="Table.TFrame")
        table_frame.pack(fill="both", expand=True, pady=(15, 0))

        self.tree = ttk.Treeview(table_frame,
            columns=('id', 'nome', 'email', 'usuario', 'cargo', 'setor', 'status'),
            show='headings',
            height=16,
            selectmode='browse'
        )

        col_config = {
            'id': {'width': 50, 'anchor': 'center'},
            'nome': {'width': 150, 'anchor': 'w'},
            'email': {'width': 180, 'anchor': 'w'},
            'usuario': {'width': 120, 'anchor': 'center'},
            'cargo': {'width': 120, 'anchor': 'center'},
            'setor': {'width': 120, 'anchor': 'center'},
            'status': {'width': 80, 'anchor': 'center'}
        }

        for col, cfg in col_config.items():
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, **cfg)

        self.tree.tag_configure('oddrow', background="#ffffff")
        self.tree.tag_configure('evenrow', background="#f2f2f2")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._abrir_edicao)

    def _carregar_colaboradores(self):
        try:
            with Database().get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
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

            for i, row in enumerate(resultados):
                status = "Ativo" if row['status'] else "Inativo"
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert('', 'end', iid=row['id'], values=(
                    row['id'], row['nome'], row['email'], row['usuario'],
                    row['cargo'], row['setor'], status
                ), tags=(tag,))
        except Error as e:
            logging.error(f"Erro de banco de dados: {e}", exc_info=True)
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
        except Exception as e:
            logging.error(f"Erro ao carregar usuários: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao carregar usuários:\n{e}")

    def _abrir_edicao(self, event):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
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
        EditarUsuarioView(top, usuario_id=None, on_save=self._carregar_colaboradores)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestão de Usuários")
    root.geometry("1000x600")

    class MockColaborador:
        def __init__(self):
            self.id = 1
            self.nome = "Admin"
            self.cargo = "ADMINISTRADOR"

    app = GerenciarUsuariosView(root, MockColaborador())
    root.mainloop()
