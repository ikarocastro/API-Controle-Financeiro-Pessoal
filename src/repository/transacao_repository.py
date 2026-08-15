from ..database.config import conectar
from ..Domain.transacao_entidades import Transacao
from ..Domain.transacao_entidades import Transacao, TipoTransacao
from datetime import date

def criar_transacao(descricao, valor, conta_id, data, tipo, categoria):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO transacao (descricao, valor, conta_id, data, tipo, categoria) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", (descricao, valor, conta_id, data, tipo.value, categoria)) # Usamos para tipo o valor do enum, que é uma string
    transacao_id = cursor.fetchone()[0] #Retornar o id da transacao criada
    conexao.commit()
    cursor.close()
    conexao.close()
    return Transacao(id = transacao_id, descricao = descricao, valor = valor, data = data, tipo = tipo, categoria = categoria)


def listar_transacoes_por_conta(conta_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM transacao WHERE conta_id = %s", (conta_id,))
    resultados = cursor.fetchall()
    transacoes = [] # Criando a lista de objetos
    for resultado in resultados:
        transacao = Transacao(id=resultado[0], descricao=resultado[2], valor=resultado[3], data=resultado[5], tipo=TipoTransacao(resultado[6]), categoria=resultado[4])
        transacoes.append(transacao)
    cursor.close()
    conexao.close()
    return transacoes

if __name__ == "__main__":
    transacoes_da_conta = listar_transacoes_por_conta(1)
for t in transacoes_da_conta:
    print(t)