from models.usuario import Colaborador
from utils.db import Database
import bcrypt


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
            ValueError: Se autenticação falhar
        """
        try:
            # 1. Busca usuário no banco
            db = Database().get_cursor()
            db.execute("""
                SELECT * FROM colaboradores 
                WHERE usuario = %s AND status = 'Ativo'
            """, (usuario,))

            dados = db.fetchone()
            if not dados:
                raise ValueError("Usuário não encontrado ou inativo")

            # 2. Cria objeto Colaborador
            colaborador = Colaborador.from_db(dados)

            # 3. Verifica senha com bcrypt
            if not bcrypt.checkpw(senha.encode(), colaborador.senha_hash.encode()):
                raise ValueError("Senha incorreta")

            # 4. Retorna usuário autenticado
            return colaborador

        except Exception as e:
            # Log detalhado do erro
            import logging
            logging.error(f"Falha na autenticação: {str(e)}", exc_info=True)
            raise ValueError("Falha durante a autenticação") from e