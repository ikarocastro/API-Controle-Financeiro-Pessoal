# API de Controle Financeiro Pessoal

Sistema de controle financeiro pessoal (uso individual, um único usuário), construído em Python com Postgres, seguindo princípios de Clean Architecture — o domínio não conhece detalhes de banco de dados, e cada camada tem uma responsabilidade única.

## Índice

- [Requisitos do projeto](#requisitos-do-projeto)
- [Arquitetura](#arquitetura)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Modelo de dados](#modelo-de-dados)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Como rodar os testes](#como-rodar-os-testes)
- [Progresso do desenvolvimento](#progresso-do-desenvolvimento)

---

## Requisitos do projeto

**Funcionais**
- RF01 — Registrar Transação
- RF02 — Consultar Saldo disponível
- RF03 — Criar uma conta
- RF04 — Ver histórico de transações

**Não funcionais**
- Persistência de dados
- Tempo de resposta inferior a 2 segundos
- Escalabilidade (documentado como boa prática, ainda que o sistema seja de uso pessoal)

---

## Arquitetura

O projeto segue uma separação em camadas inspirada em Clean Architecture:

```
Domínio (Domain/)          →  entidades e regras de negócio puras, sem
                               nenhuma dependência de banco de dados
        ↑
Repository (repository/)   →  "tradutor" entre o Domínio e o banco:
                               monta SQL, executa queries, converte
                               resultados em objetos de domínio
        ↑
Database (database/)       →  conexão com o Postgres (config.py + .env)
```

**Regra de ouro (o "teste ácido"):** trocar o banco de dados por outro não deveria exigir nenhuma mudança nas entidades ou regras do Domínio. Por isso:
- As `dataclasses` do Domínio (`Conta`, `Transacao`) não têm nenhum campo específico de banco (ex: `conta_id` como chave estrangeira só existe na tabela, não na entidade `Transacao`).
- O saldo **não é armazenado** — é sempre calculado a partir do histórico de transações (`calcular_saldo`, em `conta_regras.py`), evitando dessincronia entre saldo e histórico.
- O tipo de transação é um `Enum` Python (`TipoTransacao`) no Domínio, convertido para `VARCHAR` na hora de salvar (`.value`) e reconstruído na hora de ler (`TipoTransacao(valor)`).

---

## Estrutura de pastas

```
API-Controle-Financeiro-Pessoal/
├── .venv/                      # ambiente virtual (fora do Git)
├── .env                        # credenciais reais do banco (fora do Git)
├── .env.example                # modelo das variáveis de ambiente (no Git)
├── .gitignore
├── requirements.txt            # dependências do projeto
├── conftest.py                 # arquivo vazio — ensina o pytest a
│                                # reconhecer a raiz do projeto
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   └── config.py           # conexão com o Postgres (usa .env)
│   ├── Domain/
│   │   ├── __init__.py
│   │   ├── conta_entidades.py     # dataclass Conta (id, nome)
│   │   ├── conta_regras.py        # calcular_saldo(transacoes)
│   │   ├── transacao_entidades.py # dataclass Transacao + Enum TipoTransacao
│   │   └── transacao_regras.py    # validação de valor não-negativo
│   └── repository/
│       ├── __init__.py
│       ├── conta_repository.py       # criar_conta, buscar_conta_por_id
│       └── transacao_repository.py   # criar_transacao, listar_transacoes_por_conta
└── tests/
    ├── __init__.py
    └── test_saldo.py           # teste de integração: repository + regra de saldo
```

---

## Modelo de dados

### Tabela `conta`
```sql
CREATE TABLE conta (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(50) NOT NULL
);
```

### Tabela `transacao`
```sql
CREATE TABLE transacao(
  id SERIAL PRIMARY KEY,
  conta_id INT REFERENCES conta(id) NOT NULL,
  descricao VARCHAR(100),
  valor DECIMAL(50, 2) NOT NULL,
  categoria VARCHAR(30),
  data DATE NOT NULL,
  tipo VARCHAR(50) NOT NULL
);
```

> `tipo` foi mantido como `VARCHAR` (não `ENUM` nativo do Postgres) por ser mais simples de alterar no futuro — a validação real acontece no `Enum` do Python, no Domínio.

---

## Como rodar o projeto

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd API-Controle-Financeiro-Pessoal
```

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell)**
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
# ou, se "pip" não for reconhecido:
python3 -m pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente
Copie o `.env.example` para `.env` e preencha com as credenciais do seu Postgres local:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=api_financeiro
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

### 5. Criar o banco e as tabelas
Crie um banco de dados (ex: `api_financeiro`) no Postgres e rode os dois `CREATE TABLE` da seção [Modelo de dados](#modelo-de-dados).

### 6. Testar a conexão
```bash
python3 -m src.database.config
```
Deve exibir `conexao realizada com sucesso`.

---

## Como rodar os testes

O projeto usa [`pytest`](https://docs.pytest.org/) para testes de integração.

```bash
pytest
```

O `pytest` descobre automaticamente qualquer arquivo `test_*.py` e qualquer função `test_*` dentro dele — não é necessário apontar caminho nem usar `if __name__ == "__main__"`.

**Testando um módulo específico do Repository diretamente** (útil durante o desenvolvimento):
```bash
python3 -m src.repository.conta_repository
python3 -m src.repository.transacao_repository
```

---

## Progresso do desenvolvimento

- [x] Modelagem do domínio (requisitos, entidades, regras de negócio)
- [x] Configuração do ambiente (venv, `.gitignore`, `requirements.txt`)
- [x] Conexão com Postgres via `psycopg2` + variáveis de ambiente (`.env`)
- [x] Criação das tabelas `conta` e `transacao`
- [x] Repository de Conta: `criar_conta`, `buscar_conta_por_id`
- [x] Repository de Transação: `criar_transacao`, `listar_transacoes_por_conta`
- [x] Setup replicado em uma segunda máquina (Windows + Mac)
- [x] Testes de integração com `pytest` (Repository ↔ regra `calcular_saldo`)
- [ ] Camada de API (FastAPI)
- [ ] Validações adicionais e tratamento de erros na camada de API
- [ ] Documentação de endpoints

---

## Stack

- **Linguagem:** Python
- **Banco de dados:** PostgreSQL
- **Driver de banco:** `psycopg2-binary`
- **Variáveis de ambiente:** `python-dotenv`
- **Testes:** `pytest`
