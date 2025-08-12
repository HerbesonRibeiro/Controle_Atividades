# Versão FINAL com a correção do geometry specifier
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
from datetime import datetime
import logging
from mysql.connector import Error


class DetalhesAtividadeView:
    def __init__(self, master, atividade_id):
        self.master = master
        self.atividade_id = atividade_id
        self.db = Database()
        self.dados_para_copiar = ""

        self.master.title(f"Detalhes da Atividade #{self.atividade_id}")
        self.master.configure(bg='#f0f2f5')
        self.master.resizable(False, False)

        self.master.withdraw()

        self._configurar_estilos()
        self._carregar_e_construir_ui()

    def _centralizar_janela(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)

        # <<< CORREÇÃO FINAL >>>
        # Trocando o '+' por 'x' entre a largura e a altura.
        self.master.geometry(f'{width}x{height}+{x}+{y}')

        self.master.deiconify()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background="#f0f2f5")
        style.configure("TFrame", background="#f0f2f5")
        style.configure("Card.TFrame", background="white", relief='raised', borderwidth=1, bordercolor="#e0e0e0")
        style.configure("CardTitle.TLabel", background="white", font=("Segoe UI", 14, "bold"), foreground="#343a40")
        style.configure("Field.TLabel", background="white", font=("Segoe UI", 10), foreground="#6c757d")
        style.configure("Value.TLabel", background="white", font=("Segoe UI", 10, "bold"), foreground="#212529")
        style.configure("Descricao.TLabel", background="white", font=("Segoe UI", 10), wraplength=480)
        style.configure("Primary.TButton", background="#007bff", foreground="white", font=("Segoe UI", 10, "bold"),
                        padding=(12, 8))
        style.map("Primary.TButton", background=[("active", "#0056b3")])
        style.configure("Secondary.TButton", background="#6c757d", foreground="white", font=("Segoe UI", 10, "bold"),
                        padding=(12, 8))
        style.map("Secondary.TButton", background=[("active", "#5a6268")])

    def _carregar_e_construir_ui(self):
        try:
            query = """
                SELECT a.id, a.data_atendimento, t.nome AS tipo_atendimento, a.nivel_complexidade,
                       a.numero_atendimento, a.descricao, c.nome AS colaborador_nome, s.nome_setor
                FROM atividades a
                JOIN tipos_atendimento t ON a.tipo_atendimento_id = t.id
                JOIN colaboradores c ON a.colaborador_id = c.id
                JOIN setores s ON c.setor_id = s.id
                WHERE a.id = %s
            """
            resultados = self.db.execute_query(query, (self.atividade_id,))
            if not resultados:
                messagebox.showerror("Erro", f"Atividade com ID {self.atividade_id} não encontrada.",
                                     parent=self.master)
                self.master.destroy()
                return

            dados = resultados[0]
            self._construir_card(dados)

        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Falha ao carregar detalhes:\n{e}", parent=self.master)
            self.master.destroy()

    def _construir_card(self, dados):
        card_frame = ttk.Frame(self.master, style="Card.TFrame", padding=30)
        card_frame.pack(padx=10, pady=10, fill='both', expand=True)
        card_frame.columnconfigure(1, weight=1)

        ttk.Label(card_frame, text=f"DETALHES DA ATIVIDADE #{dados['id']}", style="CardTitle.TLabel").grid(row=0,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=(0, 15),
                                                                                                           sticky='w')
        ttk.Separator(card_frame, orient='horizontal').grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 15))

        campos_exibicao = [
            ("COLABORADOR:", dados.get('colaborador_nome')),
            ("DATA:", dados.get('data_atendimento').strftime('%d/%m/%Y') if isinstance(dados.get('data_atendimento'),
                                                                                       datetime) else "-"),
            ("SETOR:", dados.get('nome_setor')),
            ("TIPO:", dados.get('tipo_atendimento')),
            ("COMPLEXIDADE:", dados.get('nivel_complexidade')),
            ("TICKET/Nº:", dados.get('numero_atendimento')),
        ]

        row_idx = 2
        for rotulo, valor in campos_exibicao:
            self.dados_para_copiar += f"{rotulo} {str(valor).upper()}\n"
            ttk.Label(card_frame, text=rotulo, style="Field.TLabel").grid(row=row_idx, column=0, sticky='e',
                                                                          padx=(0, 10))
            ttk.Label(card_frame, text=str(valor).upper(), style="Value.TLabel").grid(row=row_idx, column=1, sticky='w')
            row_idx += 1

        ttk.Separator(card_frame, orient='horizontal').grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=15)
        row_idx += 1

        ttk.Label(card_frame, text="DESCRIÇÃO:", style="Field.TLabel").grid(row=row_idx, column=0, columnspan=2,
                                                                            sticky='w')
        row_idx += 1

        desc = dados.get('descricao')
        self.dados_para_copiar += f"\nDESCRIÇÃO:\n{desc}"

        ttk.Label(card_frame, text=desc, style="Descricao.TLabel").grid(row=row_idx, column=0, columnspan=2, sticky='w',
                                                                        pady=(5, 20))
        row_idx += 1

        btn_frame = ttk.Frame(card_frame, style="Card.TFrame")
        btn_frame.grid(row=row_idx, column=1, sticky='e', pady=(10, 0))

        ttk.Button(btn_frame, text="Fechar", command=self.master.destroy, style='Secondary.TButton').pack(side='right')
        ttk.Button(btn_frame, text="Copiar Detalhes", command=self._copiar_dados, style='Primary.TButton').pack(
            side='right', padx=(0, 10))

        self._centralizar_janela()

    def _copiar_dados(self):
        try:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.dados_para_copiar)
            messagebox.showinfo("Copiado", "Dados da atividade copiados com sucesso!", parent=self.master)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível copiar os dados:\n{e}", parent=self.master)