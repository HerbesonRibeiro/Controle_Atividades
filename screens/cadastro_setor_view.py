from tkinter import ttk, messagebox, simpledialog
from utils.db import Database

class CadastroSetorView:
    def __init__(self, master):
        self.master = master

        # 🎨 Estilos visuais
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 16, "bold"))
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Primary.TButton", background="#4a6da7", foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Primary.TButton", background=[("active", "#3a5a8a")])
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        # 🧱 Frame principal
        self.frame = ttk.Frame(master, padding=(20, 10), style="TFrame")
        self.frame.pack(fill='both', expand=True)

        # 🧑‍🏫 Título
        ttk.Label(self.frame, text="Cadastro de Setores", style="Title.TLabel")\
            .pack(anchor="center", pady=(0, 10))

        # 📦 Quadro da tabela (Frame)
        tabela_box = ttk.Frame(self.frame, style="TFrame")
        tabela_box.pack(fill="x", padx=5, pady=(0, 8))

        self.tree = ttk.Treeview(tabela_box, columns=('id', 'nome_setor'), show='headings', height=8)
        self.tree.heading('id', text='ID')
        self.tree.heading('nome_setor', text='NOME DO SETOR')
        self.tree.column('id', width=40, anchor='center')
        self.tree.column('nome_setor', width=220, anchor='w')
        self.tree.pack(fill='x', padx=5, pady=5)

        # ➕ Botões
        btn_frame = ttk.Frame(self.frame, style="TFrame")
        btn_frame.pack(pady=8)

        ttk.Button(btn_frame, text="➕ NOVO SETOR", command=self._adicionar_setor, style="Primary.TButton")\
            .pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✏️ EDITAR SETOR", command=self._editar_setor, style="TButton")\
            .pack(side='left', padx=5)

        self._carregar_setores()

    def _carregar_setores(self):
        self.tree.delete(*self.tree.get_children())
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT id, nome_setor FROM setores ORDER BY nome_setor ASC")
            setores = cursor.fetchall()
            for setor in setores:
                nome_maiusculo = setor['nome_setor'].upper()
                self.tree.insert('', 'end', values=(setor['id'], nome_maiusculo))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar setores: {e}")

    def _adicionar_setor(self):
        novo_nome = simpledialog.askstring("NOVO SETOR", "Informe o nome do novo setor:")
        if novo_nome and novo_nome.strip():
            try:
                db = Database()
                cursor = db.get_cursor()
                cursor.execute("INSERT INTO setores (nome_setor) VALUES (%s)", (novo_nome.strip(),))
                db.conn.commit()
                messagebox.showinfo("Sucesso", "Setor adicionado com sucesso.")
                self._carregar_setores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar setor: {e}")

    def _editar_setor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um setor para editar.")
            return

        item = self.tree.item(selected[0])
        setor_id, nome_atual = item['values']

        novo_nome = simpledialog.askstring("EDITAR SETOR",
                                           f"Novo nome para o setor '{nome_atual}':",
                                           initialvalue=nome_atual)
        if novo_nome and novo_nome.strip():
            try:
                db = Database()
                cursor = db.get_cursor()
                cursor.execute("UPDATE setores SET nome_setor = %s WHERE id = %s", (novo_nome.strip(), setor_id))
                db.conn.commit()
                messagebox.showinfo("Sucesso", "Setor atualizado com sucesso.")
                self._carregar_setores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar setor: {e}")