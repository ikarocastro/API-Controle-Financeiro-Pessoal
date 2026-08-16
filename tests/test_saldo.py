from src.Domain.conta_regras import calcular_saldo
from src.repository.transacao_repository import listar_transacoes_por_conta

def test_calcular_saldo():
   transacoes = listar_transacoes_por_conta(1)
   saldo = calcular_saldo(transacoes=transacoes)
   assert saldo == 200.00

if __name__ == "__main__":
   test_calcular_saldo()

   