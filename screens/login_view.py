# Arquivo: screens/login_view.py - VERSÃO FINAL
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import json
import os
import sys
from controllers.auth_controller import AuthController
from utils.db import Database

try:
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")
CAMINHO_USUARIO_SALVO = os.path.join(base_path, "ultimo_usuario.json")


class LoginView:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.controller = AuthController()
        self.db = Database()

        self.master.geometry("400x420")
        self.master.resizable(False, False)
        self.master.title("Controle de Atividades - Login")
        self.master.configure(bg='#f8f9fa')

        self.master.update_idletasks()
        x = (self.master.winfo_screenwidth() // 2) - (self.master.winfo_width() // 2)
        y = (self.master.winfo_screenheight() // 2) - (self.master.winfo_height() // 2)
        self.master.geometry(f'+{x}+{y}')

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_usuario_salvo()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", font=('Segoe UI', 10), background='#f8f9fa', foreground='#212529')
        style.configure("TFrame", background='#f8f9fa');
        style.configure("TLabel", background='#f8f9fa')
        style.configure("TCheckbutton", background='#f8f9fa')
        style.configure("Title.TLabel", font=('Segoe UI', 16, "bold"), foreground="#343a40")
        style.configure("Sub.TLabel", foreground="#6c757d")
        style.configure("Link.TLabel", foreground="#007bff", font=('Segoe UI', 9, 'underline'))
        style.configure("TEntry", padding=8)
        style.configure("Primary.TButton", font=('Segoe UI', 11, 'bold'), padding=10)
        style.configure("ShowPwd.TButton", font=('Segoe UI', 10), padding=(5, 4), relief='flat', borderwidth=0,
                        background='#e9ecef')
        style.map("ShowPwd.TButton", background=[('active', '#dce0e3')])
        style.configure("Primary.TButton", background="#007bff", foreground="white")
        style.map("Primary.TButton", background=[('active', '#0056b3')])

    def _setup_ui(self):
        self.main_frame = ttk.Frame(self.master, padding=(40, 30));
        self.main_frame.pack(expand=True, fill='both');
        self.main_frame.columnconfigure(0, weight=1)
        ttk.Label(self.main_frame, text="Bem-vindo de volta!", style="Title.TLabel").grid(row=0, column=0, pady=(0, 5),
                                                                                          sticky='w')
        ttk.Label(self.main_frame, text="Faça login para continuar", style="Sub.TLabel").grid(row=1, column=0,
                                                                                              pady=(0, 25), sticky='w')
        ttk.Label(self.main_frame, text="Usuário", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w',
                                                                                       pady=(5, 0))
        self.ent_usuario = ttk.Entry(self.main_frame, font=('Segoe UI', 10));
        self.ent_usuario.grid(row=3, column=0, sticky='ew')
        self.var_lembrar = tk.BooleanVar()
        ttk.Checkbutton(self.main_frame, text="Lembrar usuário", variable=self.var_lembrar).grid(row=4, column=0,
                                                                                                 sticky='w', pady=5)
        ttk.Label(self.main_frame, text="Senha", font=('Segoe UI', 10, 'bold')).grid(row=5, column=0, sticky='w',
                                                                                     pady=(5, 0))
        senha_frame = ttk.Frame(self.main_frame);
        senha_frame.grid(row=6, column=0, sticky='ew');
        senha_frame.columnconfigure(0, weight=1)
        self.ent_senha = ttk.Entry(senha_frame, font=('Segoe UI', 10), show="•");
        self.ent_senha.grid(row=0, column=0, sticky='ew')
        self.btn_show_pwd = ttk.Button(senha_frame, text="👁", width=3, command=self._toggle_password,
                                       style="ShowPwd.TButton");
        self.btn_show_pwd.grid(row=0, column=1, sticky='e', padx=(5, 0))
        self.btn_login = ttk.Button(self.main_frame, text="Entrar", command=self._on_login, style="Primary.TButton");
        self.btn_login.grid(row=7, column=0, sticky='ew', pady=(20, 10))
        link_senha = ttk.Label(self.main_frame, text="Esqueceu a senha?", style="Link.TLabel", cursor="hand2");
        link_senha.grid(row=8, column=0, pady=5)
        self.master.bind_all('<Return>', self._login_handler)

    def _carregar_usuario_salvo(self):
        if os.path.exists(CAMINHO_USUARIO_SALVO):
            try:
                with open(CAMINHO_USUARIO_SALVO, 'r') as f:
                    usuario = json.load(f).get("usuario")
                if usuario: self.ent_usuario.insert(0, usuario); self.var_lembrar.set(True)
            except Exception as e:
                logging.warning(f"Erro ao carregar último usuário: {e}")

    def _salvar_usuario(self):
        if self.var_lembrar.get():
            try:
                with open(CAMINHO_USUARIO_SALVO, 'w') as f:
                    json.dump({"usuario": self.ent_usuario.get().strip()}, f)
            except Exception as e:
                logging.warning(f"Erro ao salvar usuário: {e}")
        elif os.path.exists(CAMINHO_USUARIO_SALVO):
            os.remove(CAMINHO_USUARIO_SALVO)

    def _login_handler(self, event):
        if self.master.winfo_exists(): self._on_login()

    def _toggle_password(self):
        if self.ent_senha.cget('show') == '•':
            self.ent_senha.config(show='');
            self.btn_show_pwd.config(text='😑')
        else:
            self.ent_senha.config(show='•');
            self.btn_show_pwd.config(text='👁')

    def _on_login(self):
        colaborador = None
        try:
            usuario = self.ent_usuario.get().strip();
            senha = self.ent_senha.get().strip()
            if not usuario or not senha: raise ValueError("Usuário e senha são obrigatórios.")
            self.btn_login.config(state=tk.DISABLED, text="Autenticando...")
            self.master.config(cursor="watch");
            self.master.update_idletasks()
            colaborador = self.controller.autenticar(usuario, senha)
            self._salvar_usuario()
            if colaborador:
                try:
                    query = "INSERT INTO log_acessos (colaborador_id, login_timestamp, last_activity_timestamp, status) VALUES (%s, NOW(), NOW(), 'ATIVO')"
                    colaborador.session_id = self.db.execute_query(query, (colaborador.id,), fetch=False,
                                                                   lastrowid=True)
                except Exception as e:
                    logging.error(f"Falha ao registrar log de acesso: {e}")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e), parent=self.master)
        except Exception as e:
            messagebox.showerror("Erro de Autenticação", str(e), parent=self.master)
            logging.error(f"Erro no login: {e}", exc_info=True)
        finally:
            if self.master.winfo_exists(): self.btn_login.config(state=tk.NORMAL, text="Entrar"); self.master.config(
                cursor="")

        if colaborador:
            self.master.unbind_all('<Return>')
            self.on_login_success(colaborador)