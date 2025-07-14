# db.py
import mysql.connector
from mysql.connector import Error, errorcode
import os
from dotenv import load_dotenv
import time
import logging

# Configuração básica do logger (ajuste o nível conforme necessidade)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Database:
    _instance = None
    RECONNECT_DELAY = 5  # Segundos entre tentativas de reconexão
    MAX_RETRIES = 3

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conectar()
        return cls._instance

    def _conectar(self):
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                self.conn = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
                    database=os.getenv('DB_NAME'),
                    connection_timeout=30,  # Timeout em segundos
                    pool_size=5  # Opcional: para conexões simultâneas
                )
                logger.info("Conexão com o banco de dados estabelecida!")
                return
            except Error as e:
                retries += 1
                logger.error(f"Erro ao conectar (tentativa {retries}/{self.MAX_RETRIES}): {e}")
                if retries < self.MAX_RETRIES:
                    time.sleep(self.RECONNECT_DELAY)
        raise Exception("Não foi possível conectar ao banco após várias tentativas.")

    def get_cursor(self):
        try:
            return self.conn.cursor(dictionary=True)
        except mysql.connector.InterfaceError as e:
            logger.warning("Conexão perdida. Reconectando...")
            self._conectar()  # Tenta reconectar
            return self.conn.cursor(dictionary=True)