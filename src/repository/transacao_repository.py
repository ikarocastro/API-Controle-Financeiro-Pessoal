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

if __name__ == "__main__":
    nova_transacao = criar_transacao("Teste", 100.0, 1, date(2024, 8, 26), TipoTransacao.ENTRADA, "Salário")
    print(nova_transacao)