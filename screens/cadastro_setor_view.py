#revisado com conexão com db
from tkinter import ttk, messagebox, simpledialog
import tk
from utils.db import Database
import logging
from mysql.connector import Error, InterfaceError


class CadastroSetorView:
    def __init__(self, master):
        self.master = master
        self._configurar_estilos()
        self._setup_ui()
        self._carregar_setores()

    def _configurar_estilos(self):
        """Configura os estilos visuais da interface"""
        style = ttk.Style()
        style.theme_use("clam")

        # Configurações gerais
        style.configure(".", background="#f8f9fa")

        # Estilos específicos
        style.configure("TFrame", background="#f8f9fa")
        style.configure("Title.TLabel",
                        background="#f8f9fa",
                        foreground="#343a40",
                        font=("Segoe UI", 16, "bold"))
        style.configure("TLabel",
                        background="#f8f9fa",
                        font=("Segoe UI", 10))
        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"))
        style.configure("Primary.TButton",
                        background="#4a6da7",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"),
                        padding=6)
        style.map("Primary.TButton",
                  background=[("active", "#3a5a8a")])
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=25)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview",
                  background=[('selected', '#e6f3ff')])

    def _setup_ui(self):
        """Configura os componentes da interface"""
        # Frame principal
        self.frame = ttk.Frame(self.master, padding=(20, 10), style="TFrame")
        self.frame.pack(fill='both', expand=True)

        # Título
        ttk.Label(
            self.frame,
            text="Cadastro de Setores",
            style="Title.TLabel"
        ).pack(anchor="center", pady=(0, 10))

        # Frame da tabela
        tabela_frame = ttk.Frame(self.frame, style="TFrame")
        tabela_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Tabela de setores
        self._criar_tabela(tabela_frame)

        # Frame dos botões
        btn_frame = ttk.Frame(self.frame, style="TFrame")
        btn_frame.pack(fill='x', pady=(5, 0))

        # Botões
        ttk.Button(
            btn_frame,
            text="➕ Novo Setor",
            command=self._adicionar_setor,
            style="Primary.TButton"
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text="✏️ Editar Setor",
            command=self._editar_setor,
            style="TButton"
        ).pack(side='left', padx=5)

    def _criar_tabela(self, parent_frame):
        """Cria e configura a Treeview"""
        # Tabela
        self.tree = ttk.Treeview(
            parent_frame,
            columns=('id', 'nome_setor'),
            show='headings',
            height=8,
            selectmode='browse'
        )

        # Configuração das colunas
        col_config = {
            'id': {'width': 50, 'anchor': 'center', 'text': 'ID'},
            'nome_setor': {'width': 250, 'anchor': 'w', 'text': 'NOME DO SETOR'}
        }

        for col, config in col_config.items():
            self.tree.heading(col, text=config['text'])
            self.tree.column(col, width=config['width'], anchor=config['anchor'])

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(parent_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill='both', expand=True)

    def _carregar_setores(self):
        """Carrega os setores do banco de dados"""
        try:
            with Database().get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT id, nome_setor 
                        FROM setores 
                        ORDER BY nome_setor ASC
                    """)
                    setores = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())

            for setor in setores:
                self.tree.insert(
                    '',
                    'end',
                    values=(
                        setor['id'],
                        setor['nome_setor'].upper()
                    )
                )

        except Error as e:
            logging.error(f"Erro de banco de dados: {e}", exc_info=True)
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
        except Exception as e:
            logging.error(f"Erro ao carregar setores: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao carregar setores:\n{e}")

    def _adicionar_setor(self):
        """Adiciona um novo setor"""
        novo_nome = simpledialog.askstring(
            "Novo Setor",
            "Informe o nome do novo setor:",
            parent=self.master
        )

        if not novo_nome or not novo_nome.strip():
            return

        try:
            with Database().get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO setores (nome_setor) VALUES (%s)",
                        (novo_nome.strip(),)
                    )
                    conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Setor adicionado com sucesso.",
                parent=self.master
            )
            self._carregar_setores()

        except Error as e:
            logging.error(f"Erro de banco de dados: {e}", exc_info=True)
            messagebox.showerror(
                "Erro",
                "Falha na conexão com o banco de dados",
                parent=self.master
            )
        except Exception as e:
            logging.error(f"Erro ao adicionar setor: {e}", exc_info=True)
            messagebox.showerror(
                "Erro",
                f"Erro ao adicionar setor:\n{e}",
                parent=self.master
            )

    def _editar_setor(self):
        """Edita o setor selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Atenção",
                "Selecione um setor para editar.",
                parent=self.master
            )
            return

        item = self.tree.item(selected[0])
        setor_id, nome_atual = item['values']

        novo_nome = simpledialog.askstring(
            "Editar Setor",
            f"Novo nome para o setor '{nome_atual}':",
            initialvalue=nome_atual,
            parent=self.master
        )

        if not novo_nome or not novo_nome.strip():
            return

        try:
            with Database().get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE setores SET nome_setor = %s WHERE id = %s",
                        (novo_nome.strip(), setor_id)
                    )
                    conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Setor atualizado com sucesso.",
                parent=self.master
            )
            self._carregar_setores()

        except Error as e:
            logging.error(f"Erro de banco de dados: {e}", exc_info=True)
            messagebox.showerror(
                "Erro",
                "Falha na conexão com o banco de dados",
                parent=self.master
            )
        except Exception as e:
            logging.error(f"Erro ao atualizar setor: {e}", exc_info=True)
            messagebox.showerror(
                "Erro",
                f"Erro ao atualizar setor:\n{e}",
                parent=self.master
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroSetorView(root)
    root.mainloop()