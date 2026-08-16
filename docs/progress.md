# Progresso do Projeto

- Passo a Passo do projeto:

1. Folder `src`
2. Criar as pastas `Domain` e `database`
3. Criar as `Entidades` e adicionar suas `Regras`
4. Criar `config` e `.env` da database para conectar ao Postgres
5. Configurar ambiente: venv, .gitignore, requirements.txt
6. Criar as tabelas `conta` e `transacao` no Postgres
7. Criar a pasta `Repository`
8. Implementar `criar_conta`, `criar_transacao`, `buscar_conta_por_id`
9. Replicar o setup completo no Mac (``venv, imports relativos, __init__.py``)
10. Implementar ``listar_transacoes_por_conta``
11. Testar integração entre Repository e Domínio (`calcular_saldo`)

# observações da Criacão 

1. Configuração do ambiente — criação do ``venv``/``.venv``, ``.gitignore`` (com ``venv/``, ``__pycache__/``, ``.env``), e ``requirements.txt`` com ``pip freeze``. Isso foi bastante trabalho (inclusive resolveu bugs reais no Mac)

2. Criação das funções: ``criar_conta``, ``criar_transacao`` e ``buscar_conta_por_id```

3. ``Setup em duas máquinas`` — você replicou o projeto inteiro no Mac, incluindo resolver problemas de ``venv duplicado``, ``imports relativos``, ``__init__.py``(diferença entre rodar arquivo solto vs. módulo em pacote).

4. Criação da Função ``listar_transacoes_por_conta``:

- Busca todas as transações de uma conta com SELECT ... WHERE conta_id = %s
- Usa fetchall() em vez de fetchone() — traz várias linhas de uma vez, numa lista de tuplas (fetchone() só serve pra uma linha ou None)
- Percorre os resultados com um for, montando um objeto Transacao pra cada linha e adicionando numa lista com .append()
- tipo precisa ser reconstruído do Enum: o banco guarda como string ("Entrada"), então a volta é TipoTransacao(resultado[6])
- Testado com sucesso: retornou as 2 transações de teste da conta 1, com todos os campos corretos (incluindo valor já vindo como Decimal)

# Observação do tópico 11

- Criada pasta `tests/` na raiz do projeto (fora de `src/`) — teste de integração não pertence nem ao Repository nem ao Domínio isoladamente.

- Instalado `pytest (pip install pytest + atualizado requirements.txt)`.

- `pytest` reconhece automaticamente funções que começam com `test_`, sem precisar de `if __name__ == "__main__"` — só rodar pytest na raiz já descobre e executa tudo.

- Criado `tests/test_saldo.py`: busca as transações da conta 1 via `listar_transacoes_por_conta`, passa pro calcular_saldo, e confere o resultado com assert `saldo == 200.00`.

- Resultado final: `1 passed ✅``
