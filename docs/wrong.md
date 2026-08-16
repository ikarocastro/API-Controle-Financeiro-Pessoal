# Erros encontrados e corrigidos no processo:

## Erro 1 Repository + pytest

- Erro: `no tests ran`
- Causa: `Arquivo nomeado teste_saldo.py — não bate com o padrão que o pytest reconhece`
- Solução: `Renomeado para test_saldo.py (padrão: começar com test_ ou terminar com _test.py)`

- Erro: `ModuleNotFoundError: No module named 'src'`
- Causa: `pytest não sabia que a raiz do projeto era o ponto de partida pra imports`
- Solução: `Criado conftest.py vazio na raiz — só a presença do arquivo já resolve`

- Erro: `ModuleNotFoundError: No module named 'transacao_entidades'`
- Causa: `Import absoluto simples (from transacao_entidades import ...) dentro de conta_regras.py, mas o arquivo é irmão dentro da mesma pasta Domain/`
- Solução: `Trocado para import relativo: from .transacao_entidades import ...`

- Erro: `NameError: name 'transacoes_da_conta' is not defined`
- Causa: `O for de teste, no final de transacao_repository.py, estava fora da indentação do if __name__ == "__main__" — rodava mesmo quando o arquivo era só importado (não executado direto)`
- Solução: `Indentado o for/print pra dentro do if`
