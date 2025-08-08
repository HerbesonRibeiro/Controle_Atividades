# Resivado conexão com BD
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
import bcrypt
import logging
from mysql.connector import Error, InterfaceError


class EditarUsuarioView:
    def __init__(self, master, usuario_id=None, on_save=None):
        self.master = master
        self.usuario_id = usuario_id
        self.on_save = on_save
        self.dados = None

        # Configurações iniciais
        self.master.title("Editar Usuário" if usuario_id else "Novo Usuário")
        self.master.geometry("420x540")
        self.master.resizable(False, False)

        # Carrega dados iniciais
        self._carregar_dados_iniciais()
        self._setup_ui()

    def _carregar_dados_iniciais(self):
        """Carrega setores e perfis do banco de dados"""
        try:
            with Database().get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # Carrega setores
                    cursor.execute("SELECT id, nome_setor FROM setores ORDER BY nome_setor")
                    self.setores = cursor.fetchall()
                    self.setor_nomes = [s['nome_setor'] for s in self.setores]

                    # Carrega perfis
                    cursor.execute("SELECT id, nome FROM perfis ORDER BY nome")
                    self.perfis = cursor.fetchall()
                    self.perfil_nomes = [p['nome'] for p in self.perfis]

                    # Carrega dados do usuário se existir
                    if self.usuario_id:
                        cursor.execute("SELECT * FROM colaboradores WHERE id = %s", (self.usuario_id,))
                        self.dados = cursor.fetchone()

        except Error as e:
            logging.error(f"Erro de banco de dados: {e}", exc_info=True)
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
            self.master.destroy()
        except Exception as e:
            logging.error(f"Erro ao carregar dados iniciais: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")
            self.master.destroy()

    def _get_nome_setor(self):
        """Retorna o nome do setor do usuário atual"""
        if not self.dados:
            return self.setor_nomes[0] if self.setor_nomes else ""
        for s in self.setores:
            if s['id'] == self.dados['setor_id']:
                return s['nome_setor']
        return ""

    def _get_nome_perfil(self):
        """Retorna o nome do perfil do usuário atual"""
        if not self.dados:
            return self.perfil_nomes[0] if self.perfil_nomes else ""
        for p in self.perfis:
            if p['id'] == self.dados['perfil_id']:
                return p['nome']
        return ""

    def _setup_ui(self):
        """Configura a interface do usuário"""
        style = ttk.Style()
        style.theme_use("clam")

        # Configuração de estilos
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel",
                        font=('Segoe UI', 10),
                        background="#f8f9fa",
                        padding=2)
        style.configure("TEntry",
                        font=('Segoe UI', 10),
                        padding=5)
        style.configure("TCombobox",
                        font=('Segoe UI', 10))
        style.configure("Primary.TButton",
                        font=('Segoe UI', 10, 'bold'),
                        background="#4a6da7",
                        foreground="white",
                        padding=6)
        style.map("Primary.TButton",
                  background=[("active", "#3a5a8a")])

        # Container principal com scroll
        container = ttk.Frame(self.master)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg="#f8f9fa", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame de conteúdo
        frame = ttk.Frame(scrollable_frame, padding=20)
        frame.pack(fill='both', expand=True)

        # Variáveis de controle
        self.var_nome = tk.StringVar(value=self.dados['nome'] if self.dados else "")
        self.var_email = tk.StringVar(value=self.dados['email'] if self.dados else "")
        self.var_usuario = tk.StringVar(value=self.dados['usuario'] if self.dados else "")
        self.var_senha = tk.StringVar()
        self.var_cargo = tk.StringVar(value=self.dados['cargo'] if self.dados else "Colaborador")
        self.var_status = tk.StringVar(value="Ativo" if self.dados and self.dados['status'] else "Inativo")
        self.var_setor_nome = tk.StringVar(value=self._get_nome_setor())
        self.var_perfil_nome = tk.StringVar(value=self._get_nome_perfil())

        # Campos do formulário
        campos = [
            ("👤 Nome", self.var_nome),
            ("📧 E-mail", self.var_email),
            ("👥 Usuário", self.var_usuario),
            ("🔐 Nova Senha", self.var_senha, True)  # Campo de senha
        ]

        for idx, (label, var, *opts) in enumerate(campos):
            ttk.Label(frame, text=label).grid(row=idx, column=0, sticky="w", pady=(10, 0))
            if opts and opts[0]:  # Campo de senha
                ttk.Entry(frame, textvariable=var, show="*").grid(row=idx, column=1, sticky="ew", pady=(10, 0))
            else:
                ttk.Entry(frame, textvariable=var).grid(row=idx, column=1, sticky="ew", pady=(10, 0))

        # Separador
        ttk.Separator(frame).grid(row=len(campos), column=0, columnspan=2, pady=10, sticky="ew")

        # Comboboxes
        comboboxes = [
            ("📌 Cargo", self.var_cargo, ["Colaborador", "Administrador", "Coordenador", "Gestor"]),
            ("⚙️ Status", self.var_status, ["Ativo", "Inativo"]),
            ("🏢 Setor", self.var_setor_nome, self.setor_nomes),
            ("🧩 Perfil", self.var_perfil_nome, self.perfil_nomes)
        ]

        for idx, (label, var, values) in enumerate(comboboxes, start=len(campos) + 1):
            ttk.Label(frame, text=label).grid(row=idx, column=0, sticky="w", pady=(10, 0))
            ttk.Combobox(frame, textvariable=var, values=values, state="readonly").grid(
                row=idx, column=1, sticky="ew", pady=(10, 0))

        # Botão salvar
        ttk.Button(frame,
                   text="💾 Salvar Usuário",
                   style="Primary.TButton",
                   command=self._salvar).grid(
            row=len(campos) + len(comboboxes) + 1,
            column=0,
            columnspan=2,
            pady=20)

        # Configuração das colunas
        frame.columnconfigure(1, weight=1)

    def _salvar(self):
        """Salva os dados do usuário no banco de dados"""
        try:
            # Validação dos dados
            nome = self.var_nome.get().strip()
            email = self.var_email.get().strip()
            usuario = self.var_usuario.get().strip()
            senha = self.var_senha.get().strip()
            cargo = self.var_cargo.get()
            status = self.var_status.get() == "Ativo"
            setor_nome = self.var_setor_nome.get()
            perfil_nome = self.var_perfil_nome.get()

            if not nome or not email or not usuario:
                messagebox.showwarning("Aviso", "Nome, e-mail e usuário são obrigatórios.")
                return

            # Obtém IDs dos relacionamentos
            setor_id = next((s['id'] for s in self.setores if s['nome_setor'] == setor_nome), None)
            perfil_id = next((p['id'] for p in self.perfis if p['nome'] == perfil_nome), None)

            if None in (setor_id, perfil_id):
                messagebox.showerror("Erro", "Setor ou perfil inválido.")
                return

            # Para novo usuário, senha é obrigatória
            if not self.usuario_id and not senha:
                messagebox.showerror("Erro", "Senha é obrigatória para novo usuário.")
                return

            # Hash da senha se fornecida
            senha_hash = None
            if senha:
                senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

            with Database().get_connection() as conn:
                with conn.cursor() as cursor:
                    if self.usuario_id:
                        # Atualização de usuário existente
                        if senha_hash:
                            cursor.execute("""
                                UPDATE colaboradores SET 
                                    nome=%s, email=%s, usuario=%s, senha=%s,
                                    cargo=%s, status=%s, setor_id=%s, perfil_id=%s
                                WHERE id=%s
                            """, (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id,
                                  self.usuario_id))
                        else:
                            cursor.execute("""
                                UPDATE colaboradores SET 
                                    nome=%s, email=%s, usuario=%s,
                                    cargo=%s, status=%s, setor_id=%s, perfil_id=%s
                                WHERE id=%s
                            """, (nome, email, usuario, cargo, status, setor_id, perfil_id, self.usuario_id))
                    else:
                        # Inserção de novo usuário
                        cursor.execute("""
                            INSERT INTO colaboradores (
                                nome, email, usuario, senha, 
                                cargo, status, setor_id, perfil_id
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (nome, email, usuario, senha_hash, cargo, status, setor_id, perfil_id))

                    conn.commit()

            messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")
            if self.on_save:
                self.on_save()
            self.master.destroy()

        except Error as e:
            logging.error(f"Erro de banco de dados: {e}", exc_info=True)
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
        except Exception as e:
            logging.error(f"Erro ao salvar usuário: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao salvar usuário:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EditarUsuarioView(root)
    root.mainloop()