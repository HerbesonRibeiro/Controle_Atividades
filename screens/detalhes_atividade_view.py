
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
from datetime import datetime
import logging
from mysql.connector import Error, InterfaceError


class DetalhesAtividadeView:
    def __init__(self, master, atividade_id):
        self.master = master
        self.master.title("DETALHES DA ATIVIDADE")
        self.master.geometry("540x500")
        self.master.configure(bg='#f0f0f0')  # Cor de fundo mais neutra
        self.master.resizable(False, False)

        self.atividade_id = atividade_id
        self.dados_para_copiar = ""

        self._configurar_estilos()
        self._carregar_detalhes()
        self._centralizar_janela()

    def _centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'+{x}+{y}')

    def _configurar_estilos(self):
        """Configura os estilos visuais dos componentes"""
        style = ttk.Style()

        # Configuração do tema
        style.theme_use('clam')

        # Configurações gerais
        style.configure('.', background='#f0f0f0')

        # Estilos para labels
        style.configure('Bold.TLabel',
                        font=('Segoe UI', 10, 'bold'),
                        background='#f0f0f0')
        style.configure('Regular.TLabel',
                        font=('Segoe UI', 10),
                        background='#f0f0f0')
        style.configure('Valor.TLabel',
                        font=('Segoe UI', 10),
                        foreground='#0066cc',
                        background='#f0f0f0')

        # Estilo do LabelFrame
        style.configure('Detalhes.TLabelframe',
                        background='#ffffff',
                        relief='groove',
                        borderwidth=2)
        style.configure('Detalhes.TLabelframe.Label',
                        font=('Segoe UI', 11, 'bold'),
                        background='#ffffff')

        # Estilos para botões
        style.configure('Copiar.TButton',
                        font=('Segoe UI', 10, 'bold'),
                        background='#17a2b8',
                        foreground='white',
                        padding=6)
        style.map('Copiar.TButton',
                  background=[('active', '#138496'), ('!disabled', '#17a2b8')])

        style.configure('Fechar.TButton',
                        font=('Segoe UI', 10, 'bold'),
                        background='#6c757d',
                        foreground='white',
                        padding=6)
        style.map('Fechar.TButton',
                  background=[('active', '#5a6268'), ('!disabled', '#6c757d')])

    def _carregar_detalhes(self):
        """Carrega os detalhes da atividade do banco de dados"""
        try:
            with Database().get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT 
                            a.id,
                            a.data_atendimento,
                            t.nome AS tipo_atendimento,
                            a.nivel_complexidade,
                            a.numero_atendimento,
                            a.descricao,
                            c.nome AS colaborador_nome,
                            s.nome_setor
                        FROM atividades a
                        JOIN tipos_atendimento t ON a.tipo_atendimento_id = t.id
                        JOIN colaboradores c ON a.colaborador_id = c.id
                        JOIN setores s ON c.setor_id = s.id
                        WHERE a.id = %s
                    """, (self.atividade_id,))
                    dados = cursor.fetchone()

            if not dados:
                lbl_erro = ttk.Label(self.master,
                                     text="ATIVIDADE NÃO ENCONTRADA.",
                                     style='Bold.TLabel')
                lbl_erro.pack(pady=20)
                return

            # Frame principal
            main_frame = ttk.Frame(self.master, padding=10)
            main_frame.pack(fill='both', expand=True)

            # Container dos detalhes
            container = ttk.LabelFrame(main_frame,
                                       text="INFORMAÇÕES DA ATIVIDADE",
                                       style='Detalhes.TLabelframe')
            container.pack(fill='both', expand=True, padx=10, pady=10)

            # Frame interno para os dados
            data_frame = ttk.Frame(container, padding=15)
            data_frame.pack(fill='both', expand=True)

            self.dados_para_copiar = ""

            campos_exibicao = [
                ("id", "ID"),
                ("colaborador_nome", "COLABORADOR"),
                ("data_atendimento", "DATA"),
                ("tipo_atendimento", "TIPO"),
                ("nivel_complexidade", "COMPLEXIDADE"),
                ("numero_atendimento", "TICKET"),
                ("descricao", "DESCRIÇÃO"),
                ("nome_setor", "SETOR")
            ]

            for campo, rotulo in campos_exibicao:
                valor = dados.get(campo, "-")
                if campo == "data_atendimento" and isinstance(valor, datetime):
                    valor = valor.strftime('%d/%m/%Y')
                if isinstance(valor, str):
                    valor = valor.upper()

                linha = ttk.Frame(data_frame)
                linha.pack(fill='x', pady=5)

                lbl_rotulo = ttk.Label(linha,
                                       text=f"{rotulo}:",
                                       style='Bold.TLabel',
                                       width=15,
                                       anchor='e')
                lbl_rotulo.pack(side='left', padx=5)

                estilo_valor = "Valor.TLabel" if rotulo in ["TICKET", "COMPLEXIDADE"] else "Regular.TLabel"
                lbl_valor = ttk.Label(linha,
                                      text=str(valor),
                                      style=estilo_valor,
                                      anchor='w')
                lbl_valor.pack(side='left', fill='x', expand=True)

                self.dados_para_copiar += f"{rotulo}: {valor}\n"

            # Frame dos botões
            btn_frame = ttk.Frame(main_frame)
            btn_frame.pack(pady=10)

            btn_copiar = ttk.Button(btn_frame,
                                    text="COPIAR TUDO",
                                    command=self._copiar_dados,
                                    style='Copiar.TButton')
            btn_copiar.pack(side='left', padx=10)

            btn_fechar = ttk.Button(btn_frame,
                                    text="FECHAR",
                                    command=self.master.destroy,
                                    style='Fechar.TButton')
            btn_fechar.pack(side='left', padx=10)

        except Error as e:
            logging.error(f"Erro de banco de dados ao carregar detalhes: {e}", exc_info=True)
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
        except InterfaceError as e:
            logging.error(f"Erro de interface ao carregar detalhes: {e}", exc_info=True)
            messagebox.showerror("Erro", "Problema na comunicação com o banco de dados")
        except Exception as e:
            logging.error(f"Erro ao carregar detalhes: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao carregar detalhes:\n{e}")

    def _copiar_dados(self):
        """Copia os dados da atividade para a área de transferência"""
        try:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.dados_para_copiar)
            self.master.update()
            messagebox.showinfo("Copiado", "Dados da atividade copiados com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao copiar dados: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Não foi possível copiar os dados:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DetalhesAtividadeView(root, atividade_id=1)
    root.mainloop()