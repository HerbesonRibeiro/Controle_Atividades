# import tkinter as tk
# from tkinter import ttk, messagebox
# from utils.db import Database
#
# class CadastroAtividadesView(ttk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.db = Database()
#
#         self.config(width=360)
#         self.pack(fill="both", expand=True)
#         self.pack_propagate(False)
#
#         self._configurar_estilos()
#         self._setup_ui()
#         self._carregar_tipos()
#
#     def _configurar_estilos(self):
#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("TFrame", background="#f8f9fa")
#         style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40",
#                         font=("Segoe UI", 16, "bold"))
#         style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
#         style.configure("TButton", font=("Segoe UI", 10, "bold"))
#         style.configure("Primary.TButton", background="#4a6da7", foreground="white",
#                         font=("Segoe UI", 10, "bold"), padding=6)
#         style.map("Primary.TButton", background=[("active", "#3a5a8a")])
#         style.configure("Treeview", font=("Segoe UI", 10))
#         style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
#
#     def _setup_ui(self):
#         frame = ttk.Frame(self, padding=(20, 15), style="TFrame")
#         frame.pack(fill="both", expand=True)
#
#         ttk.Label(frame, text="Cadastro de Tipos de Atividade", style="Title.TLabel")\
#             .pack(anchor="center", pady=(0, 12))
#
#          # 📦 Quadro da tabela (sem título)
#         table_box = ttk.Frame(frame, style="TFrame")
#         table_box.pack(fill="x", padx=5, pady=(0, 10))
#
#         self.tree = ttk.Treeview(table_box, columns=("id", "nome"), show="headings", height=8)
#         self.tree.heading("id", text="ID")
#         self.tree.heading("nome", text="NOME")
#         self.tree.column("id", width=40, anchor="center")
#         self.tree.column("nome", width=240, anchor="w")
#         self.tree.pack(fill="x", padx=5, pady=5)
#
#         # ➕ Botões
#         btn_frame = ttk.Frame(frame, style="TFrame")
#         btn_frame.pack(pady=8)
#
#         ttk.Button(btn_frame, text="➕ NOVO", command=self._abrir_novo_tipo, style="Primary.TButton")\
#             .pack(side="left", padx=5)
#         ttk.Button(btn_frame, text="✏️ EDITAR", command=self._abrir_editar_tipo, style="TButton")\
#             .pack(side="left", padx=5)
#
#     def _carregar_tipos(self):
#         self.tree.delete(*self.tree.get_children())
#         try:
#             cursor = self.db.get_cursor()
#             cursor.execute("SELECT id, nome FROM tipos_atendimento ORDER BY id ASC")
#             for row in cursor.fetchall():
#                 nome_maiusculo = row["nome"].upper()
#                 self.tree.insert("", "end", values=(row["id"], nome_maiusculo))
#         except Exception as e:
#             messagebox.showerror("Erro", f"Erro ao carregar tipos: {e}")
#
#     def _abrir_novo_tipo(self):
#         self._abrir_janela_tipo()
#
#     def _abrir_editar_tipo(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showwarning("Atenção", "Selecione um tipo para editar.")
#             return
#
#         tipo_id, nome = self.tree.item(selected[0], "values")
#         self._abrir_janela_tipo(tipo_id, nome)
#
#     def _abrir_janela_tipo(self, tipo_id=None, nome=""):
#         janela = tk.Toplevel(self)
#         janela.title("Tipo de Atividade")
#         janela.configure(bg="#f8f9fa")
#         janela.transient(self.master)
#         janela.grab_set()
#
#         # Tamanho fixo sem geometry
#         container = ttk.Frame(janela, padding=15, style="TFrame")
#         container.pack(fill="both", expand=True)
#
#         ttk.Label(container, text="Nome da Atividade:", style="TLabel")\
#             .pack(anchor="w", pady=(0, 5))
#
#         entry_nome = ttk.Entry(container, font=("Segoe UI", 10))
#         entry_nome.pack(fill="x", pady=5)
#         entry_nome.insert(0, nome)
#         entry_nome.focus()
#
#         def salvar():
#             novo_nome = entry_nome.get().strip()
#             if not novo_nome:
#                 messagebox.showwarning("Campo obrigatório", "Informe o nome.")
#                 return
#
#             try:
#                 cursor = self.db.get_cursor()
#                 if tipo_id:
#                     cursor.execute("UPDATE tipos_atendimento SET nome=%s WHERE id=%s", (novo_nome, tipo_id))
#                 else:
#                     cursor.execute("INSERT INTO tipos_atendimento (nome) VALUES (%s)", (novo_nome,))
#                 self.db.conn.commit()
#                 self._carregar_tipos()
#                 janela.destroy()
#             except Exception as e:
#                 messagebox.showerror("Erro", f"Erro ao salvar: {e}")
#
#         ttk.Button(container, text="SALVAR", command=salvar, style="Primary.TButton")\
#             .pack(pady=10, ipadx=10)

import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database

class CadastroAtividadesView(ttk.Frame):
    def __init__(self, master: tk.Misc):  # Tipagem clara e compatível
        super().__init__(master)
        self.db = Database()

        self.config(width=360)
        self.pack(fill="both", expand=True)
        self.pack_propagate(False)

        self._setup_ui()
        self._carregar_tipos()

    def _setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40",
                        font=("Segoe UI", 16, "bold"))
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Primary.TButton", background="#4a6da7", foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Primary.TButton", background=[("active", "#3a5a8a")])
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        frame = ttk.Frame(self, padding=(20, 15), style="TFrame")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Cadastro de Tipos de Atividade", style="Title.TLabel")\
            .pack(anchor="center", pady=(0, 12))

        # Tabela sem título externo
        table_box = ttk.Frame(frame, style="TFrame")
        table_box.pack(fill="x", padx=5, pady=(0, 10))

        self.tree = ttk.Treeview(table_box, columns=("id", "nome"), show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="NOME")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nome", width=240, anchor="w")
        self.tree.pack(fill="x", padx=5, pady=5)

        btn_frame = ttk.Frame(frame, style="TFrame")
        btn_frame.pack(pady=8)

        ttk.Button(btn_frame, text="➕ NOVO", command=self._abrir_novo_tipo, style="Primary.TButton")\
            .pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✏️ EDITAR", command=self._abrir_editar_tipo, style="TButton")\
            .pack(side="left", padx=5)

    def _carregar_tipos(self):
        self.tree.delete(*self.tree.get_children())
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT id, nome FROM tipos_atendimento ORDER BY id ASC")
            for row in cursor.fetchall():
                nome_maiusculo = row["nome"].upper()
                self.tree.insert("", "end", values=(row["id"], nome_maiusculo))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tipos: {e}")

    def _abrir_novo_tipo(self):
        self._abrir_janela_tipo()

    def _abrir_editar_tipo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um tipo para editar.")
            return

        tipo_id, nome = self.tree.item(selected[0], "values")
        self._abrir_janela_tipo(tipo_id, nome)

    def _abrir_janela_tipo(self, tipo_id=None, nome=""):
        janela = tk.Toplevel(self)
        janela.title("Tipo de Atividade")
        janela.configure(bg="#f8f9fa")
        janela.transient(self.winfo_toplevel())  # Seguro, pois self é Frame vinculado à janela
        janela.grab_set()

        container = ttk.Frame(janela, padding=15, style="TFrame")
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Nome da Atividade:", style="TLabel")\
            .pack(anchor="w", pady=(0, 5))

        entry_nome = ttk.Entry(container, font=("Segoe UI", 10))
        entry_nome.pack(fill="x", pady=5)
        entry_nome.insert(0, nome)
        entry_nome.focus()

        def salvar():
            novo_nome = entry_nome.get().strip()
            if not novo_nome:
                messagebox.showwarning("Campo obrigatório", "Informe o nome.")
                return

            try:
                cursor = self.db.get_cursor()
                if tipo_id:
                    cursor.execute("UPDATE tipos_atendimento SET nome=%s WHERE id=%s", (novo_nome, tipo_id))
                else:
                    cursor.execute("INSERT INTO tipos_atendimento (nome) VALUES (%s)", (novo_nome,))
                self.db.conn.commit()
                self._carregar_tipos()
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

        ttk.Button(container, text="SALVAR", command=salvar, style="Primary.TButton")\
            .pack(pady=10, ipadx=10)