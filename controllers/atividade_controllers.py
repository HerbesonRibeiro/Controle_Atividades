from models.atividade import Atendimento


class AtendimentoController:
    @staticmethod
    def obter_tipos_atendimento():
        return Atendimento.TIPOS_ATENDIMENTO

    @staticmethod
    def obter_niveis():
        return Atendimento.NIVEL

    @staticmethod
    def obter_status():
        return Atendimento.STATUS

    @staticmethod
    def registrar_atendimento(colaborador, tipo, nivel, numero_ticket, status, descricao, data=None):
        atendimento = Atendimento(
            colaborador=colaborador,
            tipo=tipo,
            nivel=nivel,
            numero_ticket=numero_ticket,
            status=status,
            descricao=descricao,
            data=data
        )
        return atendimento.salvar()