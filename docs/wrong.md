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


## Erro 2 Falha nos imports + __init__.py

O que o `__init__.py` faz

Ele é um arquivo (geralmente vazio, ou quase) que marca uma pasta como um `pacote Python`. Sem ele, o Python trata a pasta só como `"uma pasta comum"` — e não consegue fazer certos tipos de `import relativo` (aqueles com `.` ou `..`) de dentro dela nem através dela.

Por que isso importava no seu projeto:

Lembra dos erros que você teve? Quando você tentou rodar `python3 -m src.repository.conta_repository`, o Python precisava entender que:

```
src é um pacote
repository é um pacote dentro de src
conta_repository é um módulo dentro desse pacote
```

Cada `__init__.py` (em `src/`, `src/database/`, `src/Domain/`, `src/repository/`) é o que confirma essa estrutura hierárquica pro Python. É graças a ele que imports como `from ..database.config import conectar` funcionam — o `..` só faz sentido `"subir um nível"` se o Python já sabe que aquilo tudo é uma árvore de pacotes conectados.

Resumindo: toda pasta que vai conter código que se `importa` entre si `(ou que será importada de fora)` precisa de um `__init__.py`. Por isso, `src/api/` também vai precisar do dela, assim que você criar essa pasta.

# Erro 3 Falha no Push

- Push falhou ao enviar os commits para o github falando que tinha commits que estavam no github que não estavam no meu Mac.

## Solução

- Usei o comando :

```
git pull --rebase origin main
```

- Que serve para baixar as mudanças que estão no Github e reorganizar meus commits locais por cima deles, assim mantendo o histórico mais limpo.

1. `git pull ->` busca mudancas do repositório remoto e integra com seu código atual
2. `origin ->` é o nome padrão do repositório, normalmente o Github
3. `main ->` é a branch que você quer atualizar
4. `--rebase ->` em vez de criar um novo commit de `merge`, ele coloca seus commits locais depois dos commits que vieram do Github