from ..database.config import conectar
from ..Domain.conta_entidades import Conta

def criar_conta(nome):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO conta (nome) VALUES (%s) RETURNING id", (nome,))
    conta_id = cursor.fetchone()[0] #Retornar o id da conta criada
    conexao.commit()
    cursor.close()
    conexao.close()
    return Conta(id = conta_id, nome = nome)

if __name__ == "__main__":
    nova_conta = criar_conta("Teste")
    print(nova_conta)