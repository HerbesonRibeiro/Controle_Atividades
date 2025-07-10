from datetime import datetime
from utils.db import get_db_connection


class Atendimento:
    TIPOS_ATENDIMENTO = ['TICKET', 'EMAIL', 'ATENDIMENTO A COORDENAÇÃO', 'OUTRO']
    NIVEL = ['LEVE (x1)', 'MÉDIO (x2)', 'GRAVE (x3)', 'GRAVÍSSIMO (x5)']
    STATUS = ['RESOLVIDO', 'FECHADO', 'ENCAMINHADO']

    def __init__(self, colaborador, tipo, nivel, numero_ticket, status, descricao, data=None):
        self.colaborador = colaborador
        self.data = data or datetime.now().strftime("%d/%m/%Y")
        self.tipo = tipo
        self.nivel = nivel
        self.numero_ticket = numero_ticket
        self.status = status
        self.descricao = descricao

    def salvar(self):
        """Salva o atendimento no banco de dados"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO atendimentos 
                (colaborador, data, tipo, nivel, numero_ticket, status, descricao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.colaborador, self.data, self.tipo, self.nivel,
                  self.numero_ticket, self.status, self.descricao))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar atendimento: {e}")
            return False
        finally:
            conn.close()