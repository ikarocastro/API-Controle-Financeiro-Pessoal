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

# observações da Criacão 

1. Configuração do ambiente — criação do ``venv``/``.venv``, ``.gitignore`` (com ``venv/``, ``__pycache__/``, ``.env``), e ``requirements.txt`` com ``pip freeze``. Isso foi bastante trabalho (inclusive resolveu bugs reais no Mac)

2. Criação das funções: ``criar_conta``, ``criar_transacao`` e ``buscar_conta_por_id```

3. ``Setup em duas máquinas`` — você replicou o projeto inteiro no Mac, incluindo resolver problemas de ``venv duplicado``, ``imports relativos``, ``__init__.py``(diferença entre rodar arquivo solto vs. módulo em pacote).