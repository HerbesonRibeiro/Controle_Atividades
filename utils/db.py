import os
import sys
import time
import logging
from pathlib import Path

from dotenv import load_dotenv
from cryptography.fernet import Fernet
import mysql.connector
from mysql.connector import Error, InterfaceError

# Configura log padrão
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_base_path():
    """Retorna a raiz do projeto, mesmo empacotado com PyInstaller"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

# Carrega .env da raiz do projeto (funciona no .exe)
dotenv_path = get_base_path() / ".env"

if not dotenv_path.exists():
    raise FileNotFoundError(f"Arquivo .env não encontrado em: {dotenv_path}")
load_dotenv(dotenv_path)

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Lê configurações do .env
        self.RECONNECT_DELAY = int(os.getenv("DB_RECONNECT_DELAY", 5))
        self.MAX_RETRIES     = int(os.getenv("DB_MAX_RETRIES",     3))
        self.POOL_NAME       = os.getenv("DB_POOL_NAME",           "pool1")
        self.POOL_SIZE       = int(os.getenv("DB_POOL_SIZE",       5))
        self.DB_HOST         = os.getenv("DB_HOST")
        self.DB_USER         = os.getenv("DB_USER")
        self.DB_NAME         = os.getenv("DB_NAME")
        self.DB_PORT         = int(os.getenv("DB_PORT", 3306))

        # Descriptografa a senha
        self.password = self._decrypt_password()
        self._connect()

    def _decrypt_password(self):
        try:
            raw_pass = os.getenv("DB_PASS", "").encode()
            key      = os.getenv("KEY", "").encode()
            fernet   = Fernet(key)
            decrypted = fernet.decrypt(raw_pass).decode()
            logger.info("🔑 Senha descriptografada com sucesso.")
            return decrypted
        except Exception as e:
            logger.error("❌ Falha ao descriptografar senha: %s", e)
            raise ValueError("Erro ao descriptografar a senha")

    def _connect(self):
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                self.conn = mysql.connector.connect(
                    host=self.DB_HOST,
                    user=self.DB_USER,
                    password=self.password,
                    database=self.DB_NAME,
                    port=self.DB_PORT,
                    connection_timeout=30,
                    pool_name=self.POOL_NAME,
                    pool_size=self.POOL_SIZE
                )
                logger.info("✅ Conexão com o banco de dados estabelecida!")
                return
            except Error as e:
                retries += 1
                logger.warning("❌ Erro ao conectar (tentativa %d/%d): %s", retries, self.MAX_RETRIES, e)
                time.sleep(self.RECONNECT_DELAY)

        raise ConnectionError("Não foi possível conectar ao banco após várias tentativas.")

    def get_cursor(self):
        """
        Retorna um cursor em modo dicionário. Reestabelece conexão se necessário.
        """
        try:
            if not self.conn.is_connected():
                raise InterfaceError("Conexão não está ativa.")
            return self.conn.cursor(dictionary=True)
        except InterfaceError:
            logger.warning("⚠️ Conexão perdida. Tentando reconectar...")
            self._connect()
            return self.conn.cursor(dictionary=True)

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()
            logger.info("🔒 Conexão com o banco encerrada.")

# Teste isolado
if __name__ == "__main__":
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("SELECT * FROM colaboradores")
    resultados = cursor.fetchall()
    print("Resultados da consulta:", resultados)
    db.close()

