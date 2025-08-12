# Arquivo: models/usuario.py - VERSÃO CORRIGIDA
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class Cargo(Enum):
    COLABORADOR = "Colaborador"
    ADMINISTRADOR = "Administrador"
    COORDENADOR = "Coordenador"
    GESTOR = "Gestor"


# <<< MUDANÇA: O enum de Status não é mais necessário aqui,
# pois o banco usa 'Ativo'/'Inativo' que já tratamos na GerenciarUsuariosView
# class Status(Enum):
#     ATIVO = "Ativo"
#     INATIVO = "Inativo"

@dataclass
class Colaborador:
    id: int
    nome: str
    email: str
    usuario: str
    senha_hash: str
    cargo: Cargo
    status: str  # Mudado de Enum para str para simplicidade ('Ativo'/'Inativo')
    setor_id: int
    nome_setor: str  # <<< CORREÇÃO: Campo adicionado
    perfil_id: int = 1
    perfil_nome: str = "Colaborador"
    session_id: int = None  # Útil para o log de acessos
    data_cadastro: datetime = None

    @classmethod
    def from_db(cls, db_data: dict):
        # O banco retorna 1 para 'Ativo' e 0 para 'Inativo' no campo status (TINYINT)
        # Então, convertemos para uma string mais amigável.
        status_str = "Ativo" if db_data.get('status') else "Inativo"

        return cls(
            id=db_data['id'],
            nome=db_data['nome'],
            email=db_data['email'],
            usuario=db_data['usuario'],
            senha_hash=db_data['senha'],
            cargo=Cargo(db_data['cargo']),
            status=status_str,
            setor_id=db_data['setor_id'],
            nome_setor=db_data.get('nome_setor', ''),  # <<< CORREÇÃO: Campo adicionado
            perfil_id=db_data['perfil_id'],
            perfil_nome=db_data.get('perfil_nome', 'Colaborador'),
            data_cadastro=db_data.get('data_cadastro')
        )