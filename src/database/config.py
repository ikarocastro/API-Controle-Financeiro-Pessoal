from dotenv import load_dotenv
import os
from psycopg2 import connect

load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

def conectar():
    return connect(
        host= db_host,
        port= db_port,
        dbname= db_name,
        user= db_user,
        password= db_password
    )

if __name__ == "__main__":
    conexao = conectar()
    print("conexao realizada com sucesso")
    