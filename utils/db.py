# import os
# import sys
# import time
# import logging
# from multiprocessing.forkserver import connect_to_new_process
# from pathlib import Path
# from dotenv import load_dotenv
# from cryptography.fernet import Fernet
# from mysql.connector import pooling, Error, InterfaceError
#
# # Configura o log padrão
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# def get_base_path():
#     """Retorna o caminho base do projeto, mesmo quando empacotado com PyInstaller"""
#     if getattr(sys, 'frozen', False):  # Caso esteja empacotado com pyinstaller
#         return Path(sys._MEIPASS)
#     return Path(__file__).resolve().parent.parent
#
# # Carrega o arquivo .env da raiz do projeto
# dotenv_path = get_base_path() / ".env"
# if not dotenv_path.exists():
#     raise FileNotFoundError(f"Arquivo .env não encontrado: {dotenv_path}")
# load_dotenv(dotenv_path)
#
# class Database:
#     """Classe singleton de conexão com MySQL usando connection pooling"""
#     _instance = None
#     _pool = None
#
#     def __new__(cls):
#         """Garante que só uma instância da classe seja criada"""
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._initialize()
#         return cls._instance
#
#     def _initialize(self):
#         """Inicializa as configurações e cria o pool de conexões"""
#         # Lê configurações do .env
#         self.RECONNECT_DELAY = int(os.getenv("DB_RECONNECT_DELAY", 5))
#         self.MAX_RETRIES     = int(os.getenv("DB_MAX_RETRIES", 3))
#         self.POOL_NAME       = os.getenv("DB_POOL_NAME", "pool1")
#         self.POOL_SIZE       = int(os.getenv("DB_POOL_SIZE", 10))
#         self.DB_HOST         = os.getenv("DB_HOST")
#         self.DB_USER         = os.getenv("DB_USER")
#         self.DB_NAME         = os.getenv("DB_NAME")
#         self.DB_PORT         = int(os.getenv("DB_PORT", 3306))
#
#         # Descriptografa a senha
#         self.password = self._decrypt_password()
#
#         # Cria o pool de conexões
#         self._create_pool()
#
#     def _decrypt_password(self):
#         """Descriptografa a senha usando a chave do .env"""
#         try:
#             raw_pass = os.getenv("DB_PASS", "").encode()
#             key      = os.getenv("KEY", "").encode()
#             fernet   = Fernet(key)
#             decrypted = fernet.decrypt(raw_pass).decode()
#             logger.info("🔑 Senha descriptografada com sucesso.")
#             return decrypted
#         except Exception as e:
#             logger.error("❌ Falha ao descriptografar senha: %s", e)
#             raise ValueError("Erro ao descriptografar a senha")
#
#     def _create_pool(self):
#         """Cria o pool de conexões do MySQL"""
#         retries = 0
#         while retries < self.MAX_RETRIES:
#             try:
#                 self._pool = pooling.MySQLConnectionPool(
#                     pool_name=self.POOL_NAME,
#                     pool_size=self.POOL_SIZE,
#                     pool_reset_session=True,
#                     host=self.DB_HOST,
#                     port=self.DB_PORT,
#                     user=self.DB_USER,
#                     password=self.password,
#                     database=self.DB_NAME,
#                     connection_timeout=30
#                 )
#                 logger.info("✅ Pool de conexões criado com sucesso!")
#                 return
#             except Error as e:
#                 retries += 1
#                 logger.warning("❌ Erro ao criar o pool (tentativa %d/%d): %s", retries, self.MAX_RETRIES, e)
#                 time.sleep(self.RECONNECT_DELAY)
#
#         raise ConnectionError("❌ Não foi possível criar o pool de conexões.")
#
#     def get_connection(self):
#         """
#         Retorna uma conexão do pool.
#         O ideal é usar com `with Database().get_connection() as conn:`
#         """
#         try:
#             return self._pool.get_connection()
#         except Exception as e:
#             logger.error("❌ Erro ao obter conexão do pool: %s", e)
#             raise
#
#     def release_connection(self, cursor, connection):
#         """
#         Encerra o cursor e libera a conexão de volta para o pool.
#         Isso evita conexões em estado SLEEP no banco.
#         """
#         try:
#             if cursor:
#                 cursor.close()
#             if connection:
#                 connection.close()  # devolve a conexão para o pool
#             logging.info("🔄 Conexão e cursor liberados com sucesso.")
#         except Exception as e:
#             logging.error(f"❌ Erro ao liberar conexão: {e}")
#
#     def execute_query(self, query, params=None, fetch=True):
#         """
#         Executa uma query no banco com segurança e fechamento automático dos recursos.
#         - fetch=True retorna os dados (usado para SELECTs)
#         - fetch=False apenas executa (INSERT, UPDATE, DELETE)
#         """
#         try:
#             with self.get_connection() as conn:
#                 with conn.cursor(dictionary=True) as cursor:
#                     cursor.execute(query, params)
#                     if fetch:
#                         return cursor.fetchall()
#                     conn.commit()
#                     return True
#         except Error as e:
#             logger.error("❌ Erro ao executar query: %s", e)
#             raise
#
# # Teste isolado (quando executado diretamente)
# if __name__ == "__main__":
#     print("⏳ Testando conexão com o banco de dados...")
#
#     db = Database()
#
#     try:
#         conn = db.get_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT 1")
#         result = cursor.fetchone()
#         print(f"✅ Conexão bem-sucedida: {result}")
#     except Exception as e:
#         print(f"❌ Falha na conexão: {e}")
#     finally:
#         db.release_connection(cursor, conn)
#
#
# def get_db_connection():
#     return None

# utils/db.py - VERSÃO FINAL com Lógica de Retentativa (Resiliente)
import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from mysql.connector import pooling, Error
from mysql.connector.pooling import PoolError  # <<< MUDANÇA: Importa o tipo de erro específico do pool
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_base_path():
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).resolve().parent.parent
    return base_path


dotenv_path = get_base_path() / ".env"
if not dotenv_path.exists():
    raise FileNotFoundError(f"Arquivo .env não encontrado: {dotenv_path}")
load_dotenv(dotenv_path)


class Database:
    _instance = None
    _pool = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _initialize_pool(self):
        with self._lock:
            if self._pool is not None:
                return

            logger.info("🔧 Primeira chamada ao banco. Criando pool de conexões de forma segura (thread-safe)...")

            # ... (código de descriptografar senha e config) ...
            try:
                raw_pass = os.getenv("DB_PASS", "").encode()
                key = os.getenv("KEY", "").encode()
                fernet = Fernet(key)
                password = fernet.decrypt(raw_pass).decode()
            except Exception as e:
                logger.error("❌ Falha crítica ao descriptografar senha: %s", e)
                raise ValueError("Erro ao descriptografar a senha do banco de dados.")

            config = {
                "pool_name": os.getenv("DB_POOL_NAME", "pool_unico"),
                "pool_size": int(os.getenv("DB_POOL_SIZE", 10)),
                "pool_reset_session": True,
                "host": os.getenv("DB_HOST"),
                "port": int(os.getenv("DB_PORT", 3306)),
                "user": os.getenv("DB_USER"),
                "password": password,
                "database": os.getenv("DB_NAME"),
                "connection_timeout": 20
            }

            MAX_RETRIES = int(os.getenv("DB_MAX_RETRIES", 3))
            RECONNECT_DELAY = int(os.getenv("DB_RECONNECT_DELAY", 5))

            for attempt in range(MAX_RETRIES):
                try:
                    self._pool = pooling.MySQLConnectionPool(**config)
                    logger.info("✅ Pool de conexões criado com sucesso!")
                    return
                except Error as e:
                    logger.warning(f"❌ Erro ao criar o pool (tentativa {attempt + 1}/{MAX_RETRIES}): {e}")
                    time.sleep(RECONNECT_DELAY)

            raise ConnectionError("❌ Não foi possível criar o pool de conexões após múltiplas tentativas.")

    def get_connection(self):
        if self._pool is None:
            self._initialize_pool()

        # <<< CORREÇÃO FINAL: Lógica de retentativa para pool esgotado >>>
        max_retries = 5
        wait_interval = 0.2  # Espera 200ms entre as tentativas

        for attempt in range(max_retries):
            try:
                # Tenta pegar uma conexão do pool
                return self._pool.get_connection()
            except PoolError as e:
                # Se o erro for de pool esgotado, espera e tenta de novo
                logger.warning(f"Pool esgotado. Tentativa {attempt + 1}/{max_retries}. Aguardando...")
                if attempt < max_retries - 1:
                    time.sleep(wait_interval)
                else:
                    # Se todas as tentativas falharem, lança o erro
                    logger.error("Não foi possível obter conexão do pool após múltiplas tentativas.")
                    raise e

    def execute_query(self, query, params=None, fetch=True, lastrowid=False):
        try:
            with self.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, params)
                    if fetch:
                        return cursor.fetchall()
                    conn.commit()
                    if lastrowid:
                        return cursor.lastrowid
                    return True
        except Error as e:
            logger.error(f"❌ Erro ao executar query: {e}")
            raise