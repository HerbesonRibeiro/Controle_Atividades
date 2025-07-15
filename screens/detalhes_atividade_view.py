import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import Database
from datetime import datetime
import logging


class DetalhesAtividadeView:
    def __init__(self, master, atividade_id):
        self.master = master
        self.master.title("DETALHES DA ATIVIDADE")
        self.master.geometry("540x500")
        self.master.configure(bg="#f8f9fa")  # fundo suave

        self.atividade_id = atividade_id
        self._configurar_estilos()
        self._carregar_detalhes()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Bold.TLabel", font=("Segoe UI", 10, "bold"))
        style.configure("Regular.TLabel", font=("Segoe UI", 10))
        style.configure("Valor.TLabel", font=("Segoe UI", 10, "bold"), foreground="#007bff")

        # LabelFrame personalizada
        style.configure("Envoltorio.TLabelframe", background="#ffffff")
        style.configure("Envoltorio.TLabelframe.Label", font=("Segoe UI", 11, "bold"))

    def _carregar_detalhes(self):
        try:
            cursor = Database().get_cursor()
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
                ttk.Label(self.master,
                          text="ATIVIDADE NÃO ENCONTRADA.",
                          style="Bold.TLabel",
                          foreground="gray").pack(pady=10)
                return

            container = ttk.LabelFrame(self.master,
                                       text="INFORMAÇÕES DA ATIVIDADE",
                                       padding=20,
                                       style="Envoltorio.TLabelframe")
            container.pack(fill='both', expand=True, padx=20, pady=(20, 10))

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

                linha = ttk.Frame(container)
                linha.pack(fill='x', pady=6)

                ttk.Label(linha,
                          text=f"{rotulo}:",
                          style="Bold.TLabel",
                          width=16).pack(side='left')

                estilo_valor = "Valor.TLabel" if rotulo in ["TICKET", "COMPLEXIDADE"] else "Regular.TLabel"
                ttk.Label(linha,
                          text=str(valor),
                          style=estilo_valor).pack(side='left', anchor="w")

                self.dados_para_copiar += f"{rotulo}: {valor}\n"

            # Botões
            btn_frame = ttk.Frame(self.master, padding=10)
            btn_frame.pack()

            ttk.Button(btn_frame,
                       text="COPIAR TUDO",
                       command=self._copiar_dados).pack(side='left', padx=10)

            ttk.Button(btn_frame,
                       text="FECHAR",
                       command=self.master.destroy).pack(side='left', padx=10)

        except Exception as e:
            logging.error(f"Erro ao carregar detalhes: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao carregar detalhes:\n{e}")

    def _copiar_dados(self):
        try:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.dados_para_copiar)
            self.master.update()
            messagebox.showinfo("Copiado", "Dados da atividade copiados com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao copiar dados: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Não foi possível copiar os dados:\n{e}")