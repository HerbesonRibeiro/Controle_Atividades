import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='controle_atividades'
)

cursor = conexao.cursor()
cursor.execute("SHOW TABLES;")

for tabela in cursor:
    print(tabela)

cursor.close()
conexao.close()