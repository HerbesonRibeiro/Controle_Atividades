# Exceptions (Exceções de código) quando dar erro

class UsuarioNaoEncontradoError(ValueError):
    """Erro para quando o usuário não é encontrado no banco de dados."""
    pass

class UsuarioInativoError(ValueError):
    """Erro para quando o usuário existe, mas está com status inativo."""
    pass

class SenhaIncorretaError(ValueError):
    """Erro para quando a senha informada está errada."""
    pass
