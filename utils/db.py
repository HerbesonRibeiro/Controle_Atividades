# import mysql.connector
# from mysql.connector import Error
# import os
# import time
# import logging
# from dotenv import load_dotenv, find_dotenv
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# load_dotenv(find_dotenv())
#
# class Database:
#     _instance = None
#     RECONNECT_DELAY = 5
#     MAX_RETRIES = 3
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._conectar()
#         return cls._instance
#
#     def _conectar(self):
#         retries = 0
#         while retries < self.MAX_RETRIES:
#             try:
#                 self.conn = mysql.connector.connect(
#                     host=os.getenv('DB_HOST'),
#                     user=os.getenv('DB_USER'),
#                     password=os.getenv('DB_PASS'),
#                     database=os.getenv('DB_NAME'),
#                     port=int(os.getenv('DB_PORT', 3306)),
#                     connection_timeout=30,
#                     pool_size=5,
#                     pool_name='pool1'  # nome curto para evitar erro de pool name muito longo
#                 )
#                 logger.info("Conexão com o banco de dados estabelecida!")
#                 return
#             except Error as e:
#                 retries += 1
#                 logger.error(f"Erro ao conectar (tentativa {retries}/{self.MAX_RETRIES}): {e}")
#                 if retries < self.MAX_RETRIES:
#                     time.sleep(self.RECONNECT_DELAY)
#         raise Exception("Não foi possível conectar ao banco após várias tentativas.")
#
#     def get_cursor(self):
#         try:
#             return self.conn.cursor(dictionary=True)
#         except mysql.connector.InterfaceError:
#             logger.warning("Conexão perdida. Reconectando...")
#             self._conectar()
#             return self.conn.cursor(dictionary=True)

# import os
# import time
# import logging
#
# from dotenv import load_dotenv, find_dotenv
# from cryptography.fernet import Fernet
# import mysql.connector
# from mysql.connector import Error
#
# # Configura logger
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Carrega variáveis de ambiente do .env
# load_dotenv(find_dotenv())
#
# class Database:
#     _instance = None
#
#     # Parâmetros de retry e pool (podem vir do .env também)
#     RECONNECT_DELAY = int(os.getenv("DB_RECONNECT_DELAY", 5))
#     MAX_RETRIES     = int(os.getenv("DB_MAX_RETRIES",     3))
#     POOL_NAME       = os.getenv("DB_POOL_NAME",    "pool1")
#     POOL_SIZE       = int(os.getenv("DB_POOL_SIZE",     5))
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._connect()
#         return cls._instance
#
#     def _connect(self):
#         # 1) Descriptografa a senha
#         raw_pass = os.getenv("DB_PASS", "").encode()
#         key      = os.getenv("KEY",     "").encode()
#         try:
#             fernet   = Fernet(key)
#             password = fernet.decrypt(raw_pass).decode()
#             logger.info("🔑 Senha descriptografada com sucesso.")
#         except Exception as e:
#             logger.error("❌ Falha ao descriptografar senha: %s", e)
#             raise
#
#         # 2) Tenta conectar ao MySQL com pool e retry
#         retries = 0
#         while retries < self.MAX_RETRIES:
#             try:
#                 self.conn = mysql.connector.connect(
#                     host=os.getenv("DB_HOST"),
#                     user=os.getenv("DB_USER"),
#                     password=password,
#                     database=os.getenv("DB_NAME"),
#                     port=int(os.getenv("DB_PORT", 3306)),
#                     connection_timeout=30,
#                     pool_name=self.POOL_NAME,
#                     pool_size=self.POOL_SIZE
#                 )
#                 logger.info("✅ Conexão com o banco de dados estabelecida!")
#                 return
#
#             except Error as e:
#                 retries += 1
#                 logger.error(
#                     "❌ Erro ao conectar (tentativa %d/%d): %s",
#                     retries, self.MAX_RETRIES, e
#                 )
#                 if retries < self.MAX_RETRIES:
#                     time.sleep(self.RECONNECT_DELAY)
#
#         raise ConnectionError("Não foi possível conectar ao banco após várias tentativas.")
#
#     def get_cursor(self):
#         """
#         Retorna um cursor em modo dict. Se a conexão caiu, reconecta automaticamente.
#         """
#         try:
#             return self.conn.cursor(dictionary=True)
#         except mysql.connector.InterfaceError:
#             logger.warning("⚠️ Conexão perdida. Tentando reconectar...")
#             self._connect()
#             return self.conn.cursor(dictionary=True)
#
#
# # Exemplo de uso
# if __name__ == "__main__":
#     from utils.db import Database
#
#     cursor = Database().get_cursor()
#     cursor.execute("SELECT * FROM colaboradores")
#     resultados = cursor.fetchall()
#     print("Resultados da consulta:", resultados)

import os
import time
import logging
from pathlib import Path

from dotenv import load_dotenv
from cryptography.fernet import Fernet
import mysql.connector
from mysql.connector import Error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega .env da raiz do projeto
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
if not dotenv_path.exists():
    raise FileNotFoundError(f"Arquivo .env não encontrado em: {dotenv_path}")
load_dotenv(dotenv_path)

class Database:
    _instance = None

    RECONNECT_DELAY = int(os.getenv("DB_RECONNECT_DELAY", 5))
    MAX_RETRIES     = int(os.getenv("DB_MAX_RETRIES",     3))
    POOL_NAME       = os.getenv("DB_POOL_NAME",    "pool1")
    POOL_SIZE       = int(os.getenv("DB_POOL_SIZE",     5))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        # Descriptografa senha com Fernet
        raw_pass = os.getenv("DB_PASS", "").encode()
        key      = os.getenv("KEY",    "").encode()

        try:
            fernet   = Fernet(key)
            password = fernet.decrypt(raw_pass).decode()
            logger.info("🔑 Senha descriptografada com sucesso.")
        except Exception as e:
            logger.error("❌ Falha ao descriptografar senha: %s", e)
            raise

        # Tenta conectar ao MySQL com pool e retry
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                self.conn = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=password,
                    database=os.getenv("DB_NAME"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    connection_timeout=30,
                    pool_name=self.POOL_NAME,
                    pool_size=self.POOL_SIZE
                )
                logger.info("✅ Conexão com o banco de dados estabelecida!")
                return
            except Error as e:
                retries += 1
                logger.error("❌ Erro ao conectar (tentativa %d/%d): %s",
                             retries, self.MAX_RETRIES, e)
                time.sleep(self.RECONNECT_DELAY)

        raise ConnectionError("Não foi possível conectar ao banco após várias tentativas.")

    def get_cursor(self):
        """
        Retorna um cursor em modo dict. Se a conexão caiu, reconecta automaticamente.
        """
        try:
            return self.conn.cursor(dictionary=True)
        except mysql.connector.InterfaceError:
            logger.warning("⚠️ Conexão perdida. Tentando reconectar...")
            self._connect()
            return self.conn.cursor(dictionary=True)
