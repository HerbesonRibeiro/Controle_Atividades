# Revisado conexão com o bd
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
import bcrypt
import logging
from mysql.connector import Error, InterfaceError


class PerfilView:
    def __init__(self, master, colaborador):
        self.master = master  # Agora espera-se que seja um Frame
        self.colaborador = colaborador

        # Limpa o frame antes de criar novos widgets
        self._limpar_frame()

        self._configurar_estilos()
        self._setup_ui()

    def _limpar_frame(self):
        """Remove todos os widgets do frame"""
        for widget in self.master.winfo_children():
            widget.destroy()

    def _configurar_estilos(self):
        """Configura os estilos visuais dos componentes"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configurações gerais
        style.configure('.', background='#f0f0f0')

        # Estilos para labels
        style.configure('TLabel',
                        font=('Segoe UI', 10),
                        background='#f0f0f0',
                        padding=5)
        style.configure('Bold.TLabel',
                        font=('Segoe UI', 10, 'bold'),
                        background='#f0f0f0')
        style.configure('Title.TLabel',
                        font=('Segoe UI', 16, 'bold'),
                        background='#f0f0f0',
                        foreground='#2c3e50')

        # Estilos para campos de entrada
        style.configure('TEntry',
                        font=('Segoe UI', 10),
                        padding=5)

        # Estilos para botões (em preto)
        style.configure('Primary.TButton',
                        font=('Segoe UI', 10, 'bold'),
                        background='#000000',
                        foreground='white',
                        padding=8)
        style.map('Primary.TButton',
                  background=[('active', '#333333')])

    def _setup_ui(self):
        """Configura a interface do usuário diretamente no frame"""
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Título
        ttk.Label(main_frame,
                  text="MEU PERFIL",
                  style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=10)

        # Informações do perfil
        self._criar_linha(main_frame, "Nome:", self.colaborador.nome, 1)
        self._criar_linha(main_frame, "Setor:", str(self.colaborador.setor_id), 2)
        self._criar_linha(main_frame, "Cargo:", self.colaborador.cargo.value, 3)

        # Email editável
        ttk.Label(main_frame,
                  text="Email:",
                  style='TLabel').grid(row=4, column=0, sticky='e', pady=5)
        self.var_email = tk.StringVar(value=self.colaborador.email)
        ttk.Entry(main_frame,
                  textvariable=self.var_email,
                  style='TEntry',
                  width=30).grid(row=4, column=1, sticky='we', pady=5)

        # Campos de senha
        ttk.Label(main_frame,
                  text="Nova Senha:",
                  style='TLabel').grid(row=5, column=0, sticky='e', pady=5)
        self.entry_senha = ttk.Entry(main_frame,
                                     show="*",
                                     style='TEntry')
        self.entry_senha.grid(row=5, column=1, sticky='we', pady=5)

        ttk.Label(main_frame,
                  text="Confirmar Senha:",
                  style='TLabel').grid(row=6, column=0, sticky='e', pady=5)
        self.entry_confirma = ttk.Entry(main_frame,
                                        show="*",
                                        style='TEntry')
        self.entry_confirma.grid(row=6, column=1, sticky='we', pady=5)

        # Botão salvar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame,
                   text="SALVAR ALTERAÇÕES",
                   command=self._salvar,
                   style='Primary.TButton').pack(pady=10, ipadx=20)

        # Configuração das colunas
        main_frame.columnconfigure(0, weight=1, minsize=150)
        main_frame.columnconfigure(1, weight=3)

    def _criar_linha(self, frame, titulo, valor, linha):
        """Cria uma linha de informação no perfil"""
        ttk.Label(frame,
                  text=titulo,
                  style='TLabel').grid(row=linha, column=0, sticky='e')
        ttk.Label(frame,
                  text=valor,
                  style='Bold.TLabel').grid(row=linha, column=1, sticky='w')

    def _salvar(self):
        """Salva as alterações do perfil no banco de dados"""
        try:
            email = self.var_email.get().strip()
            nova_senha = self.entry_senha.get().strip()
            confirmar = self.entry_confirma.get().strip()

            # Validação das senhas
            if nova_senha and nova_senha != confirmar:
                raise ValueError("As senhas não coincidem!")
            if nova_senha and len(nova_senha) < 6:
                raise ValueError("A senha deve ter pelo menos 6 caracteres!")

            with Database().get_connection() as conn:
                with conn.cursor() as cursor:
                    # Atualiza email
                    cursor.execute(
                        "UPDATE colaboradores SET email = %s WHERE id = %s",
                        (email, self.colaborador.id)
                    )

                    # Atualiza senha se informada
                    if nova_senha:
                        senha_hash = bcrypt.hashpw(
                            nova_senha.encode(),
                            bcrypt.gensalt()
                        ).decode()
                        cursor.execute(
                            "UPDATE colaboradores SET senha = %s WHERE id = %s",
                            (senha_hash, self.colaborador.id)
                        )

                    conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Perfil atualizado com sucesso!",
                parent=self.master
            )

            # Limpa os campos de senha
            self.entry_senha.delete(0, tk.END)
            self.entry_confirma.delete(0, tk.END)

        except ValueError as ve:
            messagebox.showerror(
                "Erro de Validação",
                str(ve),
                parent=self.master
            )
        except Error as e:
            logging.error(f"Erro de banco de dados: {e}", exc_info=True)
            messagebox.showerror(
                "Erro",
                "Falha na conexão com o banco de dados",
                parent=self.master
            )
        except Exception as e:
            logging.error(f"Erro ao atualizar perfil: {e}", exc_info=True)
            messagebox.showerror(
                "Erro",
                f"Falha ao atualizar perfil:\n{str(e)}",
                parent=self.master
            )


if __name__ == "__main__":
    # Para testar isoladamente, criamos uma janela
    root = tk.Tk()
    frame = ttk.Frame(root)
    frame.pack(fill='both', expand=True)


    class MockColaborador:
        def __init__(self):
            self.id = 1
            self.nome = "Fulano de Tal"
            self.setor_id = "TI"
            self.cargo = type('Cargo', (), {'value': 'Analista'})()
            self.email = "fulano@empresa.com"


    app = PerfilView(frame, MockColaborador())
    root.mainloop()