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


def buscar_conta_por_id(conta_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM conta WHERE id = %s", (conta_id,))
    resultado = cursor.fetchone()
    if resultado is None:
        cursor.close()
        conexao.close()
        return None
    else:
        conta = Conta(id=resultado[0], nome=resultado[1])
        cursor.close()
        conexao.close()
        return conta


if __name__ == "__main__":
    conta_encontrada = buscar_conta_por_id(1)
    print(conta_encontrada)

    conta_nao_encontrada = buscar_conta_por_id(999)
    print(conta_nao_encontrada)