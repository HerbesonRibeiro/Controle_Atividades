from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class Cargo(Enum):
    COLABORADOR = "Colaborador"
    ADMINISTRADOR = "Administrador"
    COORDENADOR = "Coordenador"
    GESTOR = "Gestor"

class Status(Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"

@dataclass
class Colaborador:
    id: int
    nome: str
    email: str
    usuario: str
    senha_hash: str
    cargo: Cargo
    status: Status
    setor_id: int
    perfil_id: int = 1
    perfil_nome: str = "Colaborador"
    data_cadastro: datetime = None

    @classmethod
    def from_db(cls, db_data: dict):
        return cls(
            id=db_data['id'],
            nome=db_data['nome'],
            email=db_data['email'],
            usuario=db_data['usuario'],
            senha_hash=db_data['senha'],
            cargo=Cargo(db_data['cargo']),
            status=Status(db_data['status']),
            setor_id=db_data['setor_id'],
            perfil_id=db_data['perfil_id'],
            perfil_nome=db_data.get('perfil_nome', 'Colaborador'),
            data_cadastro=db_data['data_cadastro']
        )