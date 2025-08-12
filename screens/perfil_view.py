# screens/perfil_view.py - VERSÃO com Card Maior e Mais Espaçoso
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
import bcrypt
import logging
from mysql.connector import Error


class PerfilView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.db = Database()

        self._limpar_frame()
        self._configurar_estilos()
        self._setup_ui()

    def _limpar_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background="#f0f2f5")
        style.configure("TFrame", background="#f0f2f5")
        style.configure("Card.TFrame", background="white", relief='raised', borderwidth=1, bordercolor="#e0e0e0")
        style.configure("Avatar.TLabel", background="white", font=("Segoe UI Symbol", 36), foreground="#007bff")
        style.configure("Nome.TLabel", background="white", font=("Segoe UI", 20, "bold"), foreground="#343a40")
        style.configure("Cargo.TLabel", background="white", font=("Segoe UI", 11), foreground="#6c757d")
        style.configure("Info.TLabel", background="white", font=("Segoe UI", 10))
        style.configure("InfoBold.TLabel", background="white", font=("Segoe UI", 10, "bold"))
        style.configure("Section.TLabel", background="white", font=("Segoe UI", 12, "bold"), foreground="#495057")
        style.configure("TEntry", padding=8, font=("Segoe UI", 10))
        style.configure("Primary.TButton", background="#007bff", foreground="white", font=("Segoe UI", 11, "bold"),
                        padding=10)
        style.map("Primary.TButton", background=[("active", "#0056b3")])

    def _setup_ui(self):
        center_frame = ttk.Frame(self.master)
        center_frame.pack(expand=True)

        # <<< AJUSTE DE TAMANHO: Aumentando o padding interno do card >>>
        card_frame = ttk.Frame(center_frame, style="Card.TFrame", padding=50)
        card_frame.pack()

        # <<< AJUSTE DE TAMANHO: Definindo uma largura mínima para o card >>>
        card_frame.columnconfigure(0, minsize=450)

        # --- Cabeçalho do Card ---
        header_frame = ttk.Frame(card_frame, style="Card.TFrame")
        header_frame.grid(row=0, column=0, pady=(0, 20), sticky='w')

        ttk.Label(header_frame, text="👤", style="Avatar.TLabel").pack(side='left', padx=(0, 20))

        name_frame = ttk.Frame(header_frame, style="Card.TFrame")
        name_frame.pack(side='left')
        ttk.Label(name_frame, text=self.colaborador.nome.upper(), style="Nome.TLabel").pack(anchor='w')
        ttk.Label(name_frame, text=self.colaborador.cargo.value, style="Cargo.TLabel").pack(anchor='w')

        ttk.Separator(card_frame, orient='horizontal').grid(row=1, column=0, sticky='ew', pady=20)

        # --- Seção de Informações ---
        info_frame = ttk.Frame(card_frame, style="Card.TFrame")
        info_frame.grid(row=2, column=0, sticky='w')
        info_frame.columnconfigure(1, weight=1)

        ttk.Label(info_frame, text="Setor:", style="Info.TLabel").grid(row=0, column=0, sticky='e', padx=(0, 10))
        ttk.Label(info_frame, text=self.colaborador.nome_setor, style="InfoBold.TLabel").grid(row=0, column=1,
                                                                                              sticky='w')

        # --- Seção de Alteração de Dados ---
        form_frame = ttk.Frame(card_frame, style="Card.TFrame")
        form_frame.grid(row=3, column=0, pady=(25, 0), sticky='ew')
        form_frame.columnconfigure(0, weight=1)

        ttk.Label(form_frame, text="Alterar E-mail", style="Section.TLabel").grid(row=0, column=0, sticky='w',
                                                                                  pady=(0, 5))
        self.var_email = tk.StringVar(value=self.colaborador.email)
        ttk.Entry(form_frame, textvariable=self.var_email).grid(row=1, column=0, sticky='ew')

        ttk.Label(form_frame, text="Alterar Senha", style="Section.TLabel").grid(row=2, column=0, sticky='w',
                                                                                 pady=(20, 5))
        self.entry_senha = ttk.Entry(form_frame, show="*")
        self.entry_senha.grid(row=3, column=0, sticky='ew', pady=(0, 5))

        self.entry_confirma = ttk.Entry(form_frame, show="*")
        self.entry_confirma.grid(row=4, column=0, sticky='ew')

        self.entry_senha.insert(0, "Nova Senha")
        self.entry_confirma.insert(0, "Confirmar Senha")

        # Placeholder text logic (melhorada)
        def on_focus_in(event):
            if event.widget.get() in ["Nova Senha", "Confirmar Senha"]:
                event.widget.delete(0, tk.END)

        def on_focus_out(event, placeholder):
            if not event.widget.get():
                event.widget.insert(0, placeholder)

        self.entry_senha.bind("<FocusIn>", on_focus_in)
        self.entry_confirma.bind("<FocusIn>", on_focus_in)
        self.entry_senha.bind("<FocusOut>", lambda e: on_focus_out(e, "Nova Senha"))
        self.entry_confirma.bind("<FocusOut>", lambda e: on_focus_out(e, "Confirmar Senha"))

        ttk.Button(form_frame, text="SALVAR ALTERAÇÕES", command=self._salvar, style="Primary.TButton").grid(row=5,
                                                                                                             column=0,
                                                                                                             sticky='ew',
                                                                                                             pady=(30,
                                                                                                                   0))

    def _salvar(self):
        try:
            email = self.var_email.get().strip()
            nova_senha = self.entry_senha.get().strip() if self.entry_senha.get() != "Nova Senha" else ""
            confirmar = self.entry_confirma.get().strip() if self.entry_confirma.get() != "Confirmar Senha" else ""

            if not email: raise ValueError("O campo de e-mail não pode ficar vazio.")
            if nova_senha and nova_senha != confirmar: raise ValueError("As senhas não coincidem!")
            if nova_senha and len(nova_senha) < 6: raise ValueError("A nova senha deve ter pelo menos 6 caracteres!")

            query_email = "UPDATE colaboradores SET email = %s WHERE id = %s"
            self.db.execute_query(query_email, (email, self.colaborador.id), fetch=False)
            self.colaborador.email = email

            if nova_senha:
                senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
                query_senha = "UPDATE colaboradores SET senha = %s WHERE id = %s"
                self.db.execute_query(query_senha, (senha_hash, self.colaborador.id), fetch=False)

            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!", parent=self.master)
            self.entry_senha.delete(0, tk.END);
            self.entry_senha.insert(0, "Nova Senha")
            self.entry_confirma.delete(0, tk.END);
            self.entry_confirma.insert(0, "Confirmar Senha")
            self.master.focus()  # Tira o foco dos campos de senha

        except ValueError as ve:
            messagebox.showwarning("Erro de Validação", str(ve), parent=self.master)
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Falha ao atualizar perfil:\n{str(e)}", parent=self.master)