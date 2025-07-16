import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
import bcrypt
import logging

class NovoUsuarioView:
    def __init__(self, master, on_save=None):
        self.master = master
        self.master.title("Novo Usuário")
        self.master.geometry("400x500")
        self.on_save = on_save

        self._setup_ui()

    def _setup_ui(self):
        frame = tk.Frame(self.master, padx=20, pady=20, bg="#f8f9fa")
        frame.pack(fill='both', expand=True)

        # Campos de entrada
        self.vars = {
            "nome": tk.StringVar(),
            "email": tk.StringVar(),
            "usuario": tk.StringVar(),
            "senha": tk.StringVar(),
            "cargo": tk.StringVar(value="Colaborador"),
            "status": tk.StringVar(value="Ativo"),
            "setor": tk.StringVar(),
            "perfil_id": tk.IntVar(value=2)
        }

        campos = [
            ("Nome", "nome"),
            ("Email", "email"),
            ("Usuário", "usuario"),
            ("Senha", "senha"),
        ]

        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, bg="#f8f9fa").grid(row=i, column=0, sticky="w", pady=5)
            show = '*' if key == "senha" else ''
            entry = ttk.Entry(frame, textvariable=self.vars[key], show=show)
            entry.grid(row=i, column=1, pady=5, sticky="we")

        # Cargo
        tk.Label(frame, text="Cargo", bg="#f8f9fa").grid(row=4, column=0, sticky="w", pady=5)
        cargos = ["Colaborador", "Administrador", "Gestor", "Coordenador"]
        ttk.Combobox(frame, textvariable=self.vars["cargo"], values=cargos, state='readonly')\
            .grid(row=4, column=1, pady=5, sticky="we")

        # Status
        tk.Label(frame, text="Status", bg="#f8f9fa").grid(row=5, column=0, sticky="w", pady=5)
        status = ["Ativo", "Inativo"]
        ttk.Combobox(frame, textvariable=self.vars["status"], values=status, state='readonly')\
            .grid(row=5, column=1, pady=5, sticky="we")

        # Setor
        tk.Label(frame, text="Setor", bg="#f8f9fa").grid(row=6, column=0, sticky="w", pady=5)
        self.combo_setor = ttk.Combobox(frame, textvariable=self.vars["setor"], state="readonly")
        self.combo_setor.grid(row=6, column=1, pady=5, sticky="we")
        self._carregar_setores()

        # Botão salvar
        ttk.Button(frame, text="Salvar", command=self._salvar).grid(
            row=7, column=0, columnspan=2, pady=20)

        frame.columnconfigure(1, weight=1)

    def _carregar_setores(self):
        try:
            cursor = Database().get_cursor()
            cursor.execute("SELECT id, nome_setor FROM setores ORDER BY nome_setor")
            self.setores = {row['nome_setor']: row['id'] for row in cursor.fetchall()}
            self.combo_setor['values'] = list(self.setores.keys())
            if self.setores:
                self.vars["setor"].set(next(iter(self.setores)))
        except Exception as e:
            logging.error(f"Erro ao carregar setores: {e}", exc_info=True)
            messagebox.showerror("Erro", "Não foi possível carregar os setores.")

    def _salvar(self):
        try:
            nome = self.vars["nome"].get().strip()
            email = self.vars["email"].get().strip()
            usuario = self.vars["usuario"].get().strip()
            senha = self.vars["senha"].get()
            cargo = self.vars["cargo"].get()
            status = self.vars["status"].get()
            setor_id = self.setores.get(self.vars["setor"].get())
            perfil_id = self.vars["perfil_id"].get()

            if not all([nome, email, usuario, senha, cargo, status, setor_id]):
                raise ValueError("Preencha todos os campos obrigatórios.")

            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

            cursor = Database().get_cursor()
            cursor.execute("""
                INSERT INTO colaboradores (nome, email, usuario, senha, cargo, status, setor_id, perfil_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id))
            Database().conn.commit()

            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
            if self.on_save:
                self.on_save()
            self.master.destroy()

        except Exception as e:
            logging.error(f"Erro ao salvar usuário: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao salvar usuário:\n{e}")
