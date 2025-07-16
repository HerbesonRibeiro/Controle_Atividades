# import tkinter as tk
# from tkinter import ttk, messagebox
# from utils.db import Database
# import bcrypt
# import logging
#
# class EditarUsuarioView:
#     def __init__(self, master, usuario_id=None, on_save=None):
#         self.master = master
#         self.usuario_id = usuario_id
#         self.on_save = on_save
#         self.db = Database()
#         self.dados = None
#
#         self.setores = self._carregar_setores()
#         self.perfis = self._carregar_perfis()
#
#         self.setor_nomes = [s['nome_setor'] for s in self.setores]
#         self.perfil_nomes = [p['nome_perfil'] for p in self.perfis]
#
#         self.master.title("Editar Usuário" if usuario_id else "Novo Usuário")
#         self.master.geometry("400x520")
#         self.master.configure(bg="#f8f9fa")
#
#         self._carregar_dados()
#         self._setup_ui()
#
#     def _carregar_setores(self):
#         try:
#             cursor = self.db.get_cursor()
#             cursor.execute("SELECT id, nome_setor FROM setores ORDER BY nome_setor")
#             return cursor.fetchall()
#         except Exception as e:
#             logging.error(f"Erro ao carregar setores: {e}")
#             return []
#
#     def _carregar_perfis(self):
#         try:
#             cursor = self.db.get_cursor()
#             cursor.execute("SELECT id, nome_perfil FROM perfis ORDER BY nome_perfil")
#             return cursor.fetchall()
#         except Exception as e:
#             logging.error(f"Erro ao carregar perfis: {e}")
#             return []
#
#     def _carregar_dados(self):
#         if not self.usuario_id:
#             return
#         try:
#             cursor = self.db.get_cursor()
#             cursor.execute("SELECT * FROM colaboradores WHERE id = %s", (self.usuario_id,))
#             self.dados = cursor.fetchone()
#         except Exception as e:
#             logging.error(f"Erro ao carregar dados do usuário: {e}", exc_info=True)
#             messagebox.showerror("Erro", "Erro ao carregar dados do usuário.")
#
#     def _get_nome_setor(self):
#         if not self.dados:
#             return self.setor_nomes[0] if self.setor_nomes else ""
#         for s in self.setores:
#             if s['id'] == self.dados['setor_id']:
#                 return s['nome_setor']
#         return ""
#
#     def _get_nome_perfil(self):
#         if not self.dados:
#             return self.perfil_nomes[0] if self.perfil_nomes else ""
#         for p in self.perfis:
#             if p['id'] == self.dados['perfil_id']:
#                 return p['nome_perfil']
#         return ""
#
#     def _setup_ui(self):
#         style = ttk.Style()
#         style.configure("TLabel", font=('Segoe UI', 10), background="#f8f9fa")
#         style.configure("TEntry", font=('Segoe UI', 10))
#         style.configure("TCombobox", font=('Segoe UI', 10))
#         style.configure("TButton", font=('Segoe UI', 10, 'bold'))
#
#         frame = tk.Frame(self.master, bg="#f8f9fa", padx=20, pady=20)
#         frame.pack(expand=True, fill="both")
#
#         # Variáveis
#         self.var_nome = tk.StringVar(value=self.dados['nome'] if self.dados else "")
#         self.var_email = tk.StringVar(value=self.dados['email'] if self.dados else "")
#         self.var_usuario = tk.StringVar(value=self.dados['usuario'] if self.dados else "")
#         self.var_senha = tk.StringVar()
#         self.var_cargo = tk.StringVar(value=self.dados['cargo'] if self.dados else "Colaborador")
#         self.var_status = tk.StringVar(value=self.dados['status'] if self.dados else "Ativo")
#         self.var_setor_nome = tk.StringVar(value=self._get_nome_setor())
#         self.var_perfil_nome = tk.StringVar(value=self._get_nome_perfil())
#
#         campos = [
#             ("👤 Nome", self.var_nome),
#             ("📧 E-mail", self.var_email),
#             ("👥 Usuário", self.var_usuario),
#             ("🔐 Nova Senha", self.var_senha),
#         ]
#
#         for label, var in campos:
#             ttk.Label(frame, text=label).pack(anchor="w", pady=(12, 0))
#             ttk.Entry(frame, textvariable=var).pack(fill="x", padx=(0, 2))
#
#         ttk.Separator(frame).pack(fill="x", pady=10)
#
#         # Cargo
#         ttk.Label(frame, text="📌 Cargo").pack(anchor="w", pady=(10, 0))
#         ttk.Combobox(frame, textvariable=self.var_cargo, values=[
#             "Colaborador", "Administrador", "Coordenador", "Gestor"
#         ], state="readonly").pack(fill="x")
#
#         # Status
#         ttk.Label(frame, text="⚙️ Status").pack(anchor="w", pady=(10, 0))
#         ttk.Combobox(frame, textvariable=self.var_status, values=["Ativo", "Inativo"], state="readonly").pack(fill="x")
#
#         # Setor
#         ttk.Label(frame, text="🏢 Setor").pack(anchor="w", pady=(10, 0))
#         ttk.Combobox(frame, textvariable=self.var_setor_nome,
#                      values=self.setor_nomes, state="readonly").pack(fill="x")
#
#         # Perfil
#         ttk.Label(frame, text="🧩 Perfil").pack(anchor="w", pady=(10, 0))
#         ttk.Combobox(frame, textvariable=self.var_perfil_nome,
#                      values=self.perfil_nomes, state="readonly").pack(fill="x")
#
#         ttk.Separator(frame).pack(fill="x", pady=15)
#
#         ttk.Button(frame, text="💾 Salvar Usuário", command=self._salvar).pack(pady=(10, 0), ipadx=10, ipady=5)
#
#     def _salvar(self):
#         try:
#             nome = self.var_nome.get().strip()
#             email = self.var_email.get().strip()
#             usuario = self.var_usuario.get().strip()
#             senha = self.var_senha.get().strip()
#             cargo = self.var_cargo.get()
#             status = self.var_status.get()
#             setor_nome = self.var_setor_nome.get()
#             perfil_nome = self.var_perfil_nome.get()
#
#             if not nome or not email or not usuario:
#                 messagebox.showwarning("Campos obrigatórios", "Nome, e-mail e usuário são obrigatórios.")
#                 return
#
#             setor_id = next((s['id'] for s in self.setores if s['nome_setor'] == setor_nome), None)
#             perfil_id = next((p['id'] for p in self.perfis if p['nome_perfil'] == perfil_nome), None)
#
#             if setor_id is None or perfil_id is None:
#                 messagebox.showerror("Erro", "Setor ou perfil inválido.")
#                 return
#
#             senha_hash = None
#             if senha:
#                 senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
#
#             cursor = self.db.get_cursor()
#
#             if self.usuario_id:
#                 if senha_hash:
#                     cursor.execute("""
#                         UPDATE colaboradores SET nome=%s, email=%s, usuario=%s, senha=%s,
#                             cargo=%s, status=%s, setor_id=%s, perfil_id=%s
#                         WHERE id=%s
#                     """, (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id, self.usuario_id))
#                 else:
#                     cursor.execute("""
#                         UPDATE colaboradores SET nome=%s, email=%s, usuario=%s,
#                             cargo=%s, status=%s, setor_id=%s, perfil_id=%s
#                         WHERE id=%s
#                     """, (nome, email, usuario, cargo, status, setor_id, perfil_id, self.usuario_id))
#             else:
#                 if not senha_hash:
#                     messagebox.showerror("Erro", "Senha é obrigatória para novo usuário.")
#                     return
#
#                 cursor.execute("""
#                     INSERT INTO colaboradores
#                         (nome, email, usuario, senha, cargo, status, setor_id, perfil_id)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                 """, (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id))
#
#             self.db.conn.commit()
#             messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")
#             if self.on_save:
#                 self.on_save()
#             self.master.destroy()
#
#         except Exception as e:
#             logging.error(f"Erro ao salvar usuário: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Falha ao salvar usuário:\n{e}")

import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
import bcrypt
import logging

class EditarUsuarioView:
    def __init__(self, master, usuario_id=None, on_save=None):
        self.master = master
        self.usuario_id = usuario_id
        self.on_save = on_save
        self.db = Database()
        self.dados = None

        self.setores = self._carregar_setores()
        self.perfis = self._carregar_perfis()

        self.setor_nomes = [s['nome_setor'] for s in self.setores]
        self.perfil_nomes = [p['nome'] for p in self.perfis]

        self.master.title("Editar Usuário" if usuario_id else "Novo Usuário")
        self.master.geometry("400x520")
        self.master.configure(bg="#f8f9fa")

        self._carregar_dados()
        self._setup_ui()

    def _carregar_setores(self):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT id, nome_setor FROM setores ORDER BY nome_setor")
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Erro ao carregar setores: {e}")
            return []

    def _carregar_perfis(self):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT id, nome FROM perfis ORDER BY nome")
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Erro ao carregar perfis: {e}")
            return []

    def _carregar_dados(self):
        if not self.usuario_id:
            return
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM colaboradores WHERE id = %s", (self.usuario_id,))
            self.dados = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erro ao carregar dados do usuário: {e}", exc_info=True)
            messagebox.showerror("Erro", "Erro ao carregar dados do usuário.")

    def _get_nome_setor(self):
        if not self.dados:
            return self.setor_nomes[0] if self.setor_nomes else ""
        for s in self.setores:
            if s['id'] == self.dados['setor_id']:
                return s['nome_setor']
        return ""

    def _get_nome_perfil(self):
        if not self.dados:
            return self.perfil_nomes[0] if self.perfil_nomes else ""
        for p in self.perfis:
            if p['id'] == self.dados['perfil_id']:
                return p['nome']
        return ""

    def _setup_ui(self):
        style = ttk.Style()
        style.configure("TLabel", font=('Segoe UI', 10), background="#f8f9fa")
        style.configure("TEntry", font=('Segoe UI', 10))
        style.configure("TCombobox", font=('Segoe UI', 10))
        style.configure("TButton", font=('Segoe UI', 10, 'bold'))

        frame = tk.Frame(self.master, bg="#f8f9fa", padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        self.var_nome = tk.StringVar(value=self.dados['nome'] if self.dados else "")
        self.var_email = tk.StringVar(value=self.dados['email'] if self.dados else "")
        self.var_usuario = tk.StringVar(value=self.dados['usuario'] if self.dados else "")
        self.var_senha = tk.StringVar()
        self.var_cargo = tk.StringVar(value=self.dados['cargo'] if self.dados else "Colaborador")
        self.var_status = tk.StringVar(value=self.dados['status'] if self.dados else "Ativo")
        self.var_setor_nome = tk.StringVar(value=self._get_nome_setor())
        self.var_perfil_nome = tk.StringVar(value=self._get_nome_perfil())

        campos = [
            ("👤 Nome", self.var_nome),
            ("📧 E-mail", self.var_email),
            ("👥 Usuário", self.var_usuario),
            ("🔐 Nova Senha", self.var_senha),
        ]

        for label, var in campos:
            ttk.Label(frame, text=label).pack(anchor="w", pady=(12, 0))
            ttk.Entry(frame, textvariable=var).pack(fill="x", padx=(0, 2))

        ttk.Separator(frame).pack(fill="x", pady=10)

        ttk.Label(frame, text="📌 Cargo").pack(anchor="w", pady=(10, 0))
        ttk.Combobox(frame, textvariable=self.var_cargo, values=[
            "Colaborador", "Administrador", "Coordenador", "Gestor"
        ], state="readonly").pack(fill="x")

        ttk.Label(frame, text="⚙️ Status").pack(anchor="w", pady=(10, 0))
        ttk.Combobox(frame, textvariable=self.var_status, values=["Ativo", "Inativo"], state="readonly").pack(fill="x")

        ttk.Label(frame, text="🏢 Setor").pack(anchor="w", pady=(10, 0))
        ttk.Combobox(frame, textvariable=self.var_setor_nome,
                     values=self.setor_nomes, state="readonly").pack(fill="x")

        ttk.Label(frame, text="🧩 Perfil").pack(anchor="w", pady=(10, 0))
        ttk.Combobox(frame, textvariable=self.var_perfil_nome,
                     values=self.perfil_nomes, state="readonly").pack(fill="x")

        ttk.Separator(frame).pack(fill="x", pady=15)
        ttk.Button(frame, text="💾 Salvar Usuário", command=self._salvar).pack(pady=(10, 0), ipadx=10, ipady=5)

    def _salvar(self):
        try:
            nome = self.var_nome.get().strip()
            email = self.var_email.get().strip()
            usuario = self.var_usuario.get().strip()
            senha = self.var_senha.get().strip()
            cargo = self.var_cargo.get()
            status = self.var_status.get()
            setor_nome = self.var_setor_nome.get()
            perfil_nome = self.var_perfil_nome.get()

            if not nome or not email or not usuario:
                messagebox.showwarning("Campos obrigatórios", "Nome, e-mail e usuário são obrigatórios.")
                return

            setor_id = next((s['id'] for s in self.setores if s['nome_setor'] == setor_nome), None)
            perfil_id = next((p['id'] for p in self.perfis if p['nome'] == perfil_nome), None)

            if setor_id is None or perfil_id is None:
                messagebox.showerror("Erro", "Setor ou perfil inválido.")
                return

            senha_hash = None
            if senha:
                senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

            cursor = self.db.get_cursor()

            if self.usuario_id:
                if senha_hash:
                    cursor.execute("""
                        UPDATE colaboradores SET nome=%s, email=%s, usuario=%s, senha=%s,
                            cargo=%s, status=%s, setor_id=%s, perfil_id=%s
                        WHERE id=%s
                    """, (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id, self.usuario_id))
                else:
                    cursor.execute("""
                        UPDATE colaboradores SET nome=%s, email=%s, usuario=%s,
                            cargo=%s, status=%s, setor_id=%s, perfil_id=%s
                        WHERE id=%s
                    """, (nome, email, usuario, cargo, status, setor_id, perfil_id, self.usuario_id))
            else:
                if not senha_hash:
                    messagebox.showerror("Erro", "Senha é obrigatória para novo usuário.")
                    return

                cursor.execute("""
                    INSERT INTO colaboradores
                        (nome, email, usuario, senha, cargo, status, setor_id, perfil_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id))

            self.db.conn.commit()
            messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")
            if self.on_save:
                self.on_save()
            self.master.destroy()

        except Exception as e:
            logging.error(f"Erro ao salvar usuário: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao salvar usuário:\n{e}")