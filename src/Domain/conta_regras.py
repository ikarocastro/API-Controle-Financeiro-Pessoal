from transacao_entidades import TipoTransacao

def calcular_saldo(transacoes):
    saldo = 0
    for transacao in transacoes:
        if (transacao.tipo == TipoTransacao.ENTRADA):
            saldo += transacao.valor
        else:
            saldo -= transacao.valor
        
    return saldo

        