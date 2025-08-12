# Versão com Layout do Formulário Corrigido e Otimizado
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
import bcrypt
import logging
from mysql.connector import Error


class EditarUsuarioView:
    def __init__(self, master, usuario_id=None, on_save=None):
        self.master = master
        self.usuario_id = usuario_id
        self.on_save = on_save
        self.dados = None
        self.db = Database()

        # <<< AJUSTE: Janela mais larga para acomodar melhor o formulário >>>
        self.master.title("Editar Usuário" if usuario_id else "Novo Usuário")
        self.master.geometry("580x550")
        self.master.resizable(False, False)
        self.master.configure(bg="#f8f9fa")

        self._configurar_estilos()
        self._carregar_dados_iniciais()
        self._setup_ui()
        self._centralizar_janela()

    def _centralizar_janela(self):
        self.master.update_idletasks()
        x = (self.master.winfo_screenwidth() // 2) - (self.master.winfo_width() // 2)
        y = (self.master.winfo_screenheight() // 2) - (self.master.winfo_height() // 2)
        self.master.geometry(f'+{x}+{y}')

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f8f9fa")
        style.configure("Title.TLabel", background="#f8f9fa", foreground="#343a40", font=("Segoe UI", 16, "bold"))
        style.configure("TLabel", background="#f8f9fa")
        # <<< AJUSTE: Novo estilo para o texto de ajuda (pequeno e cinza) >>>
        style.configure("Helper.TLabel", background="#f8f9fa", foreground="#6c757d", font=("Segoe UI", 8))
        style.configure("TEntry", padding=5)
        style.configure("TCombobox")
        style.configure("Primary.TButton", background="#007bff", foreground="white", font=("Segoe UI", 10, "bold"),
                        padding=(12, 8))
        style.map("Primary.TButton", background=[("active", "#0056b3")])

    def _carregar_dados_iniciais(self):
        try:
            self.setores = self.db.execute_query("SELECT id, nome_setor FROM setores ORDER BY nome_setor")
            self.setor_nomes = [s['nome_setor'] for s in self.setores]
            self.perfis = self.db.execute_query("SELECT id, nome FROM perfis ORDER BY nome")
            self.perfil_nomes = [p['nome'] for p in self.perfis]
            if self.usuario_id:
                resultados = self.db.execute_query("SELECT * FROM colaboradores WHERE id = %s", (self.usuario_id,))
                self.dados = resultados[0] if resultados else None
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Falha ao carregar dados iniciais:\n{e}",
                                 parent=self.master)
            self.master.destroy()

    def _get_nome_setor(self):
        if not self.dados: return self.setor_nomes[0] if self.setor_nomes else ""
        return next((s['nome_setor'] for s in self.setores if s['id'] == self.dados['setor_id']), "")

    def _get_nome_perfil(self):
        if not self.dados: return self.perfil_nomes[0] if self.perfil_nomes else ""
        return next((p['nome'] for p in self.perfis if p['id'] == self.dados['perfil_id']), "")

    def _setup_ui(self):
        main_frame = ttk.Frame(self.master, padding=(25, 20))
        main_frame.pack(fill='both', expand=True)
        main_frame.rowconfigure(1, weight=0)  # <<< AJUSTE: Apenas a linha do botão irá expandir
        main_frame.columnconfigure(0, weight=1)

        title_text = "✏️ Editar Usuário" if self.usuario_id else "➕ Novo Usuário"
        ttk.Label(main_frame, text=title_text, style="Title.TLabel").grid(row=0, column=0, pady=(0, 20), sticky='w')

        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=1, column=0, sticky='nsew')
        # <<< AJUSTE: Dando mais peso para a coluna da direita (Entry) >>>
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=3)

        self.var_nome = tk.StringVar(value=self.dados['nome'] if self.dados else "")
        self.var_email = tk.StringVar(value=self.dados['email'] if self.dados else "")
        self.var_usuario = tk.StringVar(value=self.dados['usuario'] if self.dados else "")
        self.var_senha = tk.StringVar()
        self.var_cargo = tk.StringVar(value=self.dados['cargo'] if self.dados else "Colaborador")
        self.var_status = tk.StringVar(value="Ativo" if self.dados and self.dados['status'] else "Inativo")
        self.var_setor_nome = tk.StringVar(value=self._get_nome_setor())
        self.var_perfil_nome = tk.StringVar(value=self._get_nome_perfil())

        row_idx = 0
        campos = [("Nome Completo:", self.var_nome), ("E-mail:", self.var_email),
                  ("Usuário (para login):", self.var_usuario)]
        for label, var in campos:
            ttk.Label(form_frame, text=label).grid(row=row_idx, column=0, sticky="w", pady=4, padx=(0, 10))
            ttk.Entry(form_frame, textvariable=var).grid(row=row_idx, column=1, sticky="ew", pady=4)
            row_idx += 1

        # <<< AJUSTE: Label curta + texto de ajuda separado >>>
        senha_label = "Nova Senha:" if self.usuario_id else "Senha:"
        ttk.Label(form_frame, text=senha_label).grid(row=row_idx, column=0, sticky="w", pady=4, padx=(0, 10))
        ttk.Entry(form_frame, textvariable=self.var_senha, show="*").grid(row=row_idx, column=1, sticky="ew", pady=4)
        row_idx += 1

        if self.usuario_id:
            ttk.Label(form_frame, text="(Deixe em branco para não alterar)", style="Helper.TLabel").grid(row=row_idx,
                                                                                                         column=1,
                                                                                                         sticky="w",
                                                                                                         padx=0)
            row_idx += 1

        comboboxes = [("Cargo:", self.var_cargo, ["Colaborador", "Administrador", "Coordenador", "Gestor"]),
                      ("Status:", self.var_status, ["Ativo", "Inativo"]),
                      ("Setor:", self.var_setor_nome, self.setor_nomes),
                      ("Perfil:", self.var_perfil_nome, self.perfil_nomes)]
        for label, var, values in comboboxes:
            ttk.Label(form_frame, text=label).grid(row=row_idx, column=0, sticky="w", pady=4, padx=(0, 10))
            ttk.Combobox(form_frame, textvariable=var, values=values, state="readonly").grid(row=row_idx, column=1,
                                                                                             sticky="ew", pady=4)
            row_idx += 1

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, pady=(20, 0), sticky='e')
        ttk.Button(btn_frame, text="Salvar Alterações", style="Primary.TButton", command=self._salvar).pack()

    def _salvar(self):
        try:
            nome = self.var_nome.get().strip();
            email = self.var_email.get().strip();
            usuario = self.var_usuario.get().strip()
            senha = self.var_senha.get().strip();
            cargo = self.var_cargo.get();
            status = self.var_status.get()
            setor_nome = self.var_setor_nome.get();
            perfil_nome = self.var_perfil_nome.get()

            if not all([nome, email, usuario, setor_nome, perfil_nome]):
                raise ValueError("Nome, e-mail, usuário, setor e perfil são obrigatórios.")

            setor_id = next((s['id'] for s in self.setores if s['nome_setor'] == setor_nome), None)
            perfil_id = next((p['id'] for p in self.perfis if p['nome'] == perfil_nome), None)
            if setor_id is None or perfil_id is None:
                raise ValueError("Setor ou perfil selecionado é inválido.")

            if not self.usuario_id and not senha:
                raise ValueError("Senha é obrigatória para um novo usuário.")

            if self.usuario_id:
                if senha:
                    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
                    query = "UPDATE colaboradores SET nome=%s, email=%s, usuario=%s, senha=%s, cargo=%s, status=%s, setor_id=%s, perfil_id=%s WHERE id=%s"
                    params = (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id, self.usuario_id)
                else:
                    query = "UPDATE colaboradores SET nome=%s, email=%s, usuario=%s, cargo=%s, status=%s, setor_id=%s, perfil_id=%s WHERE id=%s"
                    params = (nome, email, usuario, cargo, status, setor_id, perfil_id, self.usuario_id)
            else:
                senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
                query = "INSERT INTO colaboradores (nome, email, usuario, senha, cargo, status, setor_id, perfil_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                params = (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id)

            self.db.execute_query(query, params, fetch=False)
            messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!", parent=self.master)
            if self.on_save: self.on_save()
            self.master.destroy()

        except ValueError as ve:
            messagebox.showwarning("Aviso de Validação", str(ve), parent=self.master)
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar o usuário:\n{e}",
                                 parent=self.master)