# Arquivo: teste_stress.py
import threading
import time
import random
from utils.db import Database  # Importa sua classe de banco de dados
from mysql.connector import Error

# --- Configurações do Teste ---
NUMERO_DE_REQUISICOES_SIMULTANEAS = 30  # Simula 30 'cliques' ao mesmo tempo
TEMPO_MAXIMO_DE_ESPERA = 10  # Segundos que cada requisição espera por uma conexão


def fazer_consulta(thread_id):
    """
    Esta função simula um único usuário fazendo uma consulta rápida.
    Ela será executada por cada uma de nossas threads.
    """
    try:
        print(f"[Thread {thread_id:02d}] Tentando obter conexão do pool...")

        # Usamos o seu método seguro, que já tem o 'with' para garantir a liberação
        db = Database()
        # Uma query bem simples e rápida, apenas para testar a conexão
        resultado = db.execute_query("SELECT 1+1 AS teste")

        if resultado:
            print(f"✅ [Thread {thread_id:02d}] Consulta bem-sucedida! Resultado: {resultado[0]['teste']}")
        else:
            print(f"⚠️ [Thread {thread_id:02d}] Consulta executou, mas não retornou resultado.")

        # Simula um pequeno tempo de 'trabalho' antes de a thread terminar
        time.sleep(random.uniform(0.1, 0.5))

    except Error as e:
        print(f"❌ [Thread {thread_id:02d}] ERRO DE BANCO DE DADOS: {e}")
    except Exception as e:
        print(f"❌ [Thread {thread_id:02d}] ERRO INESPERADO: {e}")


if __name__ == "__main__":
    print("🚀 Iniciando teste de estresse no pool de conexões...")
    print(f"Pool Size (Tamanho do Pool): {Database().POOL_SIZE}")  # Mostra o tamanho do seu pool
    print(f"Simulando {NUMERO_DE_REQUISICOES_SIMULTANEAS} requisições...")
    print("-" * 40)

    threads = []
    for i in range(NUMERO_DE_REQUISICOES_SIMULTANEAS):
        # Cria uma thread para cada 'usuário'
        thread = threading.Thread(target=fazer_consulta, args=(i + 1,))
        threads.append(thread)
        thread.start()  # Inicia a thread

    # Espera todas as threads terminarem
    for thread in threads:
        thread.join()

    print("-" * 40)
    print("✅ Teste de estresse concluído!")