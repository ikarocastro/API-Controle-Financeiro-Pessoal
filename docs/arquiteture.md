# Arquitetura

- Vou utilzar a Arquitetura limpa (Clean Arquiteture) para esse projeto

## Por que Clean Arquiteture?

O problema que a Clean Architecture resolve:
Se você escrever a lógica de "adicionar uma transação" misturada com o código que salva no banco de dados, você criou um acoplamento. Se um dia trocar SQLite por Postgres, ou adicionar cache, você vai ter que reescrever a regra de negócio também. A ideia é que a regra de negócio (domínio) não saiba nem que existe banco de dados.

## Quais Camadas serão utilizadas?

```Domain``` — as entidades puras (ex: Transacao, Conta) e as regras (ex: "não pode sacar mais do que o saldo"). Zero dependência de FastAPI, banco, nada.<br>
```Application``` (Use Cases) — orquestra o domínio (ex: CriarTransacaoUseCase), mas ainda não sabe como os dados são persistidos — só conhece uma interface (porta).<br>
```Infrastructure``` — implementa essa interface de verdade (ex: TransacaoRepositorySQLite).<br>
```API (FastAPI)``` — só recebe requisições HTTP e chama os use cases.<br>

## Alguns conceitos

- ````Arquitetura de Software:```` cada parte do código deve ter um motivo pra mudar. Se você mistura tudo num arquivo só, uma mudança na regra de negócio pode acabar mexendo sem querer na parte que salva no banco, por exemplo.

- ````Domínio```` = onde moram tanto as entidades (a estrutura de Conta e Transação) quanto as regras de negócio que giram em torno delas — porque a regra "não pode ter valor negativo" é uma regra do próprio domínio financeiro, não depende de nada externo (nem de banco, nem de API).

## Organização

Responsabilidades que existem no sistema até agora."o que cada parte precisa fazer":

````Alguma coisa precisa representar os dados```` — ou seja, o que é uma Conta e o que é uma Transação (as classes/estruturas que a gente já modelou).<br>
````Alguma coisa precisa conter as regras```` — tipo "não pode registrar uma transação com valor negativo diretamente", "o saldo é a soma das transações".<br>
````Alguma coisa precisa guardar os dados de verdade```` — seja em um arquivo, seja num banco.<br>
````Alguma coisa precisa receber comandos de fora```` — seja um menu no terminal, seja uma rota de API.<br>

## Organização de pastas

````Dominío````: Onde ficarão as Entidades e as Regras de negócio
 ````
dominio/
  conta_entidade.py
  conta_regras.py
  transacao_entidade.py
  transacao_regras.py
 ````
Cada entidade tem seu par (estrutura + regra), tudo dentro de dominio/.

- Dominío pronto:
- Tudo funcional!
```
conta_entidades.py — estrutura da Conta
transacao_entidades.py — estrutura da Transação + Enum TipoTransacao
transacao_regras.py — validação de valor negativo
conta_regras.py — cálculo de saldo
```
- Cada uma dessas funções faz uma coisa só, sem depender de banco de dados ou API — puro domínio, testável isoladamente.

```Repository```: ele fica no meio do caminho, conhecendo tanto o domínio (Conta, Transacao) quanto os detalhes de banco (Postgres), mas fazendo com que o domínio nunca precise saber que ele existe. É basicamente um "tradutor".

- psycopg2 (ou sua versão mais nova, psycopg) é a biblioteca mais usada em Python pra conversar com Postgres. Como ela não vem instalada por padrão no Python (diferente de dataclasses, enum, datetime, que são da "biblioteca padrão"), precisa instalar ela separadamente usando o pip — o gerenciador de pacotes do Python.

comando:
```
pip install psycopg2-binary
```

# Venv

O que é ``venv``

``venv (virtual environment / ambiente virtual)`` é um recurso nativo do Python que cria um ambiente isolado para as dependências de um projeto específico. Cada projeto tem seu próprio Python "isolado" e suas próprias bibliotecas instaladas, sem interferir no Python global da máquina nem em outros projetos.

``Para que serve``

Evita conflito de versões entre projetos diferentes (ex: Projeto A precisa da lib X versão 1.0, Projeto B precisa da versão 2.0 — sem venv, isso quebraria um dos dois).
Mantém o Python "global" da máquina limpo, sem acúmulo de pacotes de projetos diferentes.
Facilita reproduzir o ambiente em outra máquina, listando exatamente as dependências que aquele projeto usa.
Equivalente conceitual a dependências isoladas por projeto em outras linguagens (ex: um node_modules por projeto em JS, ou o escopo de dependências do Maven em Java).

``Como usar``

Ação	Comando ``(Windows / PowerShell)``<br>
Criar o ambiente	``py -m venv venv``<br>
Ativar o ambiente	``.\venv\Scripts\Activate.ps1``<br>
Instalar um pacote (com venv ativo)	``pip install nome_do_pacote``<br>
Ver pacotes instalados	``pip freeze``<br>
Salvar dependências num arquivo	``pip freeze > requirements.txt``<br>
Instalar a partir desse arquivo (em outra máquina)	``pip install -r requirements``.txt<br>
Desativar o ambiente	``deactivate``<br>

``Boas práticas``

A pasta ``venv/`` nunca deve ir para o ``Git (fica no .gitignore)`` — ela é recriável a partir do ``requirements.txt``.
O ``requirements.txt``, sim, deve ser versionado — é ele que documenta pra qualquer pessoa (ou você mesmo, em outra máquina) quais pacotes instalar pra rodar o projeto.

``O que fazer?``

- Antes de rodar esse comando: você ainda não instalou o psycopg2-binary de fato (paramos pra fazer o resumo do venv). Faz sentido rodar pip freeze > requirements.txt antes de instalar o pacote, ou depois? Pensa no propósito do arquivo — ele deveria refletir o quê exatamente?

- o arquivo requirements.txt deve refletir o que o projeto realmente usa, então só faz sentido gerá-lo depois de instalar as dependências, senão ele ficaria vazio (ou incompleto).

```
ordem certa é:

Instalar o pacote: ```pip install psycopg2-binary```
Só depois: ```pip freeze > requirements.txt```
```

roda o comando pra registrar essa dependência:
```
pip freeze > requirements.txt
```


# Ferramentas

1. ``BRmodelo`` - Modelagem de tabelas SQL
2. ``VsCode`` - IDE para desenvolvimento
3. ``Draw.IO`` - Para entidades e casos de uso
4. ``Excalidraw`` - Para modelagem do sistema em diagrama

## DataBase

- ``config.py`` = responsável só por montar a conexão com o Postgres — sem ainda misturar isso com o Repository (que vai fazer os ``SELECT``/``INSERT`` de verdade)

### Estrutura 

- importar ``load_dotenv`` do pacote ``dotenv``, e os (esse já vem na biblioteca padrão do Python, lembra de datetime, enum?)<br>
- Chamar ``load_dotenv()`` — isso vai ler o arquivo .env da raiz do projeto<br>
- Importar também a função connect do ``psycopg2``, que é quem realmente abre a conexão com o banco<br>
- Usar ``os.getenv``("DB_HOST") (e as outras chaves) pra montar os parâmetros da conexão<br>

### Connect

Agora vamos usar essas variáveis pra realmente abrir a conexão com o ``connect`` do psycopg2. A função connect recebe esses parâmetros como argumentos nomeados: ``host``, ``port``, ``dbname``, ``user``, ``password``.

- ``encapsular`` numa função dá controle sobre quando a conexão acontece, em vez de ser um efeito colateral automático de só importar o arquivo.

## Repository

- o Repository é a peça que vai usar a função conectar() do config.py pra realmente conversar com o banco — inserir uma Conta nova, buscar transações de uma conta, etc. — sem que o Domain/ (suas classes Conta, Transacao, TipoTransacao) precise saber nada sobre Postgres.

# Test

- ``teste`` não pertence a nenhuma das duas camadas, então merece viver em outro lugar, não misturado com o código de produção do ``Repository`` ou do ``Domínio.`` 

- separar ``src/`` (código-fonte de produção) de uma área de testes é exatamente como projetos profissionais se organizam. ``src/`` fica "puro", só com o que realmente compõe o sistema.