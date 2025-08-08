# from models.usuario import Colaborador
# from utils.db import Database
# import bcrypt
# import logging
# from utils.exceptions import UsuarioNaoEncontradoError, UsuarioInativoError, SenhaIncorretaError
#
# class AuthController:
#     def autenticar(self, usuario: str, senha: str) -> Colaborador:
#         cursor = None
#         conn = None
#         try:
#             # 1. Pega conexão e cursor com dicionário para facilitar o acesso
#             conn = Database().get_connection()
#             cursor = conn.cursor(dictionary=True)
#
#             # 2. Executa a consulta
#             cursor.execute("""
#                 SELECT c.*, p.nome AS perfil_nome
#                 FROM colaboradores c
#                 JOIN perfis p ON c.perfil_id = p.id
#                 WHERE c.usuario = %s AND c.status = 'Ativo'
#             """, (usuario,))
#
#             dados = cursor.fetchone()
#             if not dados:
#                 raise ValueError("Usuário não encontrado ou inativo")
#
#             # 3. Cria objeto Colaborador
#             colaborador = Colaborador.from_db(dados)
#
#             # 4. Verifica senha com bcrypt
#             if not bcrypt.checkpw(senha.encode(), colaborador.senha_hash.encode()):
#                 raise ValueError("Senha incorreta")
#
#             # 5. Retorna colaborador autenticado
#             return colaborador
#
#         except Exception as e:
#             logging.error(f"Falha na autenticação: {str(e)}", exc_info=True)
#             raise ValueError("Falha durante a autenticação") from e
#
#         finally:
#             # Liberar conexão e cursor
#             Database().release_connection(cursor, conn)
from models.usuario import Colaborador
from utils.db import Database
from utils.exceptions import UsuarioNaoEncontradoError, UsuarioInativoError, SenhaIncorretaError
import bcrypt
import logging


class AuthController:
    def autenticar(self, usuario: str, senha: str) -> Colaborador:
        """
        Autentica um usuário no sistema.

        Args:
            usuario: Nome de usuário
            senha: Senha não criptografada

        Returns:
            Objeto Colaborador autenticado

        Raises:
            UsuarioNaoEncontradoError, UsuarioInativoError, SenhaIncorretaError
        """
        cursor = None
        conn = None
        try:
            conn = Database().get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT c.*, p.nome AS perfil_nome
                FROM colaboradores c
                JOIN perfis p ON c.perfil_id = p.id
                WHERE c.usuario = %s
            """, (usuario,))

            dados = cursor.fetchone()
            if not dados:
                raise UsuarioNaoEncontradoError("Usuário não encontrado.\nEntre em contato com o Administador.")

            if dados["status"] != "Ativo":
                raise UsuarioInativoError("Usuário inativo,\nEntre em contato com o Administador.")

            colaborador = Colaborador.from_db(dados)

            if not bcrypt.checkpw(senha.encode(), colaborador.senha_hash.encode()):
                raise SenhaIncorretaError("Senha incorreta.")

            return colaborador

        except (UsuarioNaoEncontradoError, UsuarioInativoError, SenhaIncorretaError):
            raise  # Deixa que o código que chamou lida com isso (como a view)
        except Exception as e:
            logging.error(f"❌ Falha inesperada na autenticação: {str(e)}", exc_info=True)
            raise ValueError("Erro interno durante a autenticação.")
        finally:
            Database().release_connection(cursor, conn)
