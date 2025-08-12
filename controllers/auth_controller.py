# Versão FINAL e Refatorada
from models.usuario import Colaborador
from utils.db import Database
from utils.exceptions import UsuarioNaoEncontradoError, UsuarioInativoError, SenhaIncorretaError
import bcrypt
import logging


class AuthController:
    def autenticar(self, usuario: str, senha: str) -> Colaborador:
        """
        Autentica um usuário no sistema usando o método seguro e centralizado.
        """
        # <<< MUDANÇA: Não precisamos mais de 'cursor' ou 'conn' aqui >>>
        try:
            # <<< MUDANÇA: Instanciamos a classe Database >>>
            db = Database()

            query = """
                SELECT c.*, p.nome AS perfil_nome, s.nome_setor
                FROM colaboradores c
                JOIN perfis p ON c.perfil_id = p.id
                JOIN setores s ON c.setor_id = s.id
                WHERE c.usuario = %s
            """

            # <<< MUDANÇA: Usamos execute_query para buscar os dados >>>
            # Ele retorna uma lista de resultados.
            resultados = db.execute_query(query, (usuario,))

            if not resultados:
                raise UsuarioNaoEncontradoError("Usuário não encontrado.\nEntre em contato com o Administrador.")

            # Como sabemos que o usuário é único, pegamos o primeiro item da lista
            dados_do_usuario = resultados[0]

            if dados_do_usuario["status"] != "Ativo":
                raise UsuarioInativoError("Usuário inativo.\nEntre em contato com o Administrador.")

            colaborador = Colaborador.from_db(dados_do_usuario)

            if not bcrypt.checkpw(senha.encode(), colaborador.senha_hash.encode()):
                raise SenhaIncorretaError("Senha incorreta.")

            return colaborador

        except (UsuarioNaoEncontradoError, UsuarioInativoError, SenhaIncorretaError) as e:
            # Relança as exceções de negócio para a LoginView tratar
            raise e
        except Exception as e:
            logging.error(f"❌ Falha inesperada na autenticação: {str(e)}", exc_info=True)
            # Lança um erro genérico para a View, para não expor detalhes internos
            raise Exception("Erro interno durante a autenticação. Verifique os logs.")

        # <<< MUDANÇA: O bloco 'finally' com release_connection foi removido >>>
        # O 'execute_query' já cuida disso automaticamente para nós.