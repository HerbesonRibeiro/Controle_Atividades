import tkinter as tk
from utils.db import Database

class DetalhesAtividadeView:
    def __init__(self, master, atividade_id):
        self.master = master
        self.master.title("Detalhes da Atividade")
        self.master.geometry("500x400")
        self.atividade_id = atividade_id

        self._carregar_detalhes()

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
                    a.descricao
                FROM atividades a
                JOIN tipos_atendimento t ON a.tipo_atendimento_id = t.id
                WHERE a.id = %s
            """, (self.atividade_id,))
            dados = cursor.fetchone()

            if not dados:
                tk.Label(self.master, text="Atividade não encontrada.").pack(pady=10)
                return

            # Container para os detalhes
            container = tk.Frame(self.master, padx=20, pady=20)
            container.pack(fill='both', expand=True)

            for k, v in dados.items():
                nome_campo = k.replace("_", " ").capitalize()
                valor = v if v is not None else "-"
                texto = f"{nome_campo}: {valor}"
                tk.Label(container, text=texto, anchor="w", justify="left", font=("Segoe UI", 10)).pack(fill='x', pady=5)

        except Exception as e:
            tk.Label(self.master, text=f"Erro ao carregar: {str(e)}", fg="red").pack(pady=10)
