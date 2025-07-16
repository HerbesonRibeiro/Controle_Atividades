# import tkinter as tk
# from tkinter import ttk, messagebox
# from utils.db import Database
# import bcrypt
#
#
# class PerfilView:
#     def __init__(self, master, colaborador):
#         self.master = master
#         self.colaborador = colaborador
#         self.db = Database()
#
#         self._setup_ui()
#
#     def _setup_ui(self):
#         frame = tk.Frame(self.master, bg="#f8f9fa", padx=20, pady=20)
#         frame.pack(expand=True, fill='both')
#
#         tk.Label(frame, text="Meu Perfil", font=('Segoe UI', 16, 'bold'),
#                  bg="#f8f9fa").grid(row=0, column=0, columnspan=2, pady=10)
#
#         self._criar_linha(frame, "Nome:", self.colaborador.nome, 1)
#         self._criar_linha(frame, "Setor:", str(self.colaborador.setor_id), 2)
#         self._criar_linha(frame, "Cargo:", self.colaborador.cargo.value, 3)
#
#         # Email editável
#         tk.Label(frame, text="Email:", bg="#f8f9fa").grid(row=4, column=0, sticky="e", pady=5)
#         self.var_email = tk.StringVar(value=self.colaborador.email)
#         ttk.Entry(frame, textvariable=self.var_email, width=40).grid(row=4, column=1, sticky="w")
#
#         # Campos de senha
#         tk.Label(frame, text="Nova Senha:", bg="#f8f9fa").grid(row=5, column=0, sticky="e", pady=5)
#         self.entry_senha = ttk.Entry(frame, show="*")
#         self.entry_senha.grid(row=5, column=1, sticky="w")
#
#         tk.Label(frame, text="Confirmar Senha:", bg="#f8f9fa").grid(row=6, column=0, sticky="e", pady=5)
#         self.entry_confirma = ttk.Entry(frame, show="*")
#         self.entry_confirma.grid(row=6, column=1, sticky="w")
#
#         # Botão salvar
#         ttk.Button(frame, text="Salvar Alterações", command=self._salvar).grid(
#             row=7, column=0, columnspan=2, pady=20)
#
#     def _criar_linha(self, frame, titulo, valor, linha):
#         tk.Label(frame, text=titulo, bg="#f8f9fa").grid(row=linha, column=0, sticky="e", pady=5)
#         tk.Label(frame, text=valor, bg="#f8f9fa", font=("Segoe UI", 10, "bold")).grid(
#             row=linha, column=1, sticky="w")
#
#     def _salvar(self):
#         try:
#             email = self.var_email.get().strip()
#             nova_senha = self.entry_senha.get().strip()
#             confirmar = self.entry_confirma.get().strip()
#
#             if nova_senha and nova_senha != confirmar:
#                 raise ValueError("As senhas não coincidem.")
#
#             cursor = self.db.get_cursor()
#
#             # Atualiza email
#             cursor.execute("UPDATE colaboradores SET email = %s WHERE id = %s", (email, self.colaborador.id))
#
#             # Atualiza senha se informada
#             if nova_senha:
#                 senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
#                 cursor.execute("UPDATE colaboradores SET senha = %s WHERE id = %s", (senha_hash, self.colaborador.id))
#
#             self.db.conn.commit()
#             messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
#
#         except Exception as e:
#             messagebox.showerror("Erro", f"Falha ao atualizar: {e}")

import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
import bcrypt

class PerfilView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.db = Database()

        self._configurar_estilos()
        self._setup_ui()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 12))
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 18, "bold"))
        style.configure("TEntry", font=("Segoe UI", 12))
        style.configure("Primary.TButton", background="#4a6da7", foreground="white",
                        font=("Segoe UI", 12, "bold"), padding=8)
        style.map("Primary.TButton", background=[("active", "#3a5a8a")])

    def _setup_ui(self):
        frame = ttk.Frame(self.master, padding=20, style="TFrame")
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text="Meu Perfil", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=10)

        self._criar_linha(frame, "Nome:", self.colaborador.nome, 1)
        self._criar_linha(frame, "Setor:", str(self.colaborador.setor_id), 2)
        self._criar_linha(frame, "Cargo:", self.colaborador.cargo.value, 3)

        # Email editável
        ttk.Label(frame, text="Email:").grid(row=4, column=0, sticky="e", pady=5)
        self.var_email = tk.StringVar(value=self.colaborador.email)
        ttk.Entry(frame, textvariable=self.var_email, width=40).grid(row=4, column=1, sticky="w")

        # Nova senha
        ttk.Label(frame, text="Nova Senha:").grid(row=5, column=0, sticky="e", pady=5)
        self.entry_senha = ttk.Entry(frame, show="*")
        self.entry_senha.grid(row=5, column=1, sticky="w")

        # Confirmação
        ttk.Label(frame, text="Confirmar Senha:").grid(row=6, column=0, sticky="e", pady=5)
        self.entry_confirma = ttk.Entry(frame, show="*")
        self.entry_confirma.grid(row=6, column=1, sticky="w")

        # Botão salvar
        ttk.Button(frame, text="Salvar Alterações", command=self._salvar,
                   style="Primary.TButton").grid(row=7, column=0, columnspan=2, pady=20)

        frame.columnconfigure(1, weight=1)

    def _criar_linha(self, frame, titulo, valor, linha):
        ttk.Label(frame, text=titulo).grid(row=linha, column=0, sticky="e", pady=5)
        ttk.Label(frame, text=valor, font=("Segoe UI", 10, "bold")).grid(row=linha, column=1, sticky="w")

    def _salvar(self):
        try:
            email = self.var_email.get().strip()
            nova_senha = self.entry_senha.get().strip()
            confirmar = self.entry_confirma.get().strip()

            if nova_senha and nova_senha != confirmar:
                raise ValueError("As senhas não coincidem.")

            cursor = self.db.get_cursor()
            cursor.execute("UPDATE colaboradores SET email = %s WHERE id = %s", (email, self.colaborador.id))

            if nova_senha:
                senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
                cursor.execute("UPDATE colaboradores SET senha = %s WHERE id = %s",
                               (senha_hash, self.colaborador.id))

            self.db.conn.commit()
            messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")