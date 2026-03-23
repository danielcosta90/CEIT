import psycopg2

def conectar():
    conexao = psycopg2.connect(
        host="localhost",
        database="ceit_db",
        user="ceit_user",
        password="123456"
    )
    conexao.set_client_encoding('UTF8')
    return conexao