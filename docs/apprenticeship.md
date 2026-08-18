# Aprendizado durante o processo de Criação

## DataClass

- ````Uma data class (classe de dados)```` em Python é uma classe usada principalmente para armazenar dados. O decorador ````@dataclass```` gera automaticamente métodos comuns como ``__init__ (construtor)``, ````__repr__ (representação em texto)````  e ```__eq__ (comparação)```, eliminando códigos repetitivos (boilerplate)

Ex:

isto
```
Class Conta
def __init__(self, id: int, nome: str):
    self.id = id
    self.nome = nome
```
se torna isto:
```
@dataclass
class Conta:
    id: int
    nome: str
```

## Instanciando a classe

### O que é instanciar?
- Instanciar uma classe em Python significa criar um objeto concreto a partir do molde definido na classe. A classe funciona como a planta de uma casa, enquanto a instância é a casa construída com cores e móveis reais. Para isso, chama-se a classe como se fosse uma função (objeto = Classe())

## Enum

- Em Python, existe uma ferramenta feita exatamente pra isso: o ``Enum (enumeração)`` — ele permite você dizer "esse campo só pode ser um desses valores fixos, e nada mais". O próprio editor/IDE também passa a te ajudar com autocomplete, porque ele sabe exatamente quais são as opções válidas.

## DateTime

- Para trabalhar com datas em Python, use a biblioteca embutida chamada datetime, Dentro dele existem alguns tipos.

## Raise (error)

- valor não pode ser negativo. Isso não é mais um campo de dado (como fizemos até agora) — é comportamento, ou seja, vira uma função.

- Em Python, "impedir de continuar e avisar que algo deu errado" se faz lançando uma exceção ``(raise)``.
- A forma mais simples em Python é usar uma exceção já existente na linguagem, chamada ``ValueError`` — ela existe justamente pra representar "um valor não é válido pro que eu esperava".
---
Estrutura Básica:
```
raise ValueError("mensagem explicando o que deu errado")
```
- Nomes de função se escrevem em letra ``mínuscula``, e as de classes com letra ``maiúscula``, isso se chama ``snake_case``
---
Lógica da função:
```
def validar_error(valor):
    if (valor < 0):
        raise ValueError("O numero digitado não é aceito por ser negativo!")
```

- Se o valor = 50, ele não entra no loop passa direto e continua o código, se for valor = -10, entra no if e é interrompido!

## Função de calcular saldo

```
def calcular_saldo(transacoes):
    saldo = 0
    for transacao in transacoes:
        if (transacao.tipo == TipoTransacao.ENTRADA):
            saldo += transacao.valor
        else:
            saldo -= transacao.valor
        
    return saldo
```

- Repara a diferença: agora a função só recebe uma coisa de fora — a lista de transações — e ela mesma decide, internamente, que todo cálculo começa do zero. Ninguém de fora pode influenciar o ponto de partida. Isso é mais seguro pro que a função representa (calcular o saldo puro, baseado só no histórico real)

---
# PostgreSQL

- Usarei o ``VARCHAR`` para fazer a autenticação no banco de ``ENTRADA`` e ``SAÍDA`` dos dados, já que utilizar o ENUM do postgre não seria uma boa ideia pois num futuro próximo poderia ter que alterar para add mais alguma finalidade, como o domínio já tem o enum para a validação utilizarei o varchar no postgre que só precisarei adicionar mais uma linha.

# Env

- Usado para manter segurança

-  ``.env`` (assim como venv/) entra no .gitignore — ele nunca vai pro GitHub. Só o seu código Python (que só referencia as chaves, tipo os.getenv("DB_PASSWORD"), sem nunca escrever a senha de verdade) é que fica público. Cada pessoa que for rodar o projeto cria seu próprio .env localmente, com suas próprias credenciais.

- Por isso, geralmente também se cria um segundo arquivo, chamado .env.example (esse sim vai pro Git), que mostra quais chaves existem, mas sem os valores reais — só como documentação de "o que você precisa preencher".

- Em vez de escrever senha = "1234" direto no código Python, você escreve isso num arquivo separado chamado .env, que fica na raiz do projeto

- Repara: é só CHAVE=valor, uma por linha, sem aspas, sem espaços ao redor do =

- Sozinho, o Python não sabe ler um arquivo .env — precisa de uma biblioteca externa pra isso, chamada ``python-dotenv``. Ela lê o arquivo .env e "injeta" essas chaves como variáveis de ambiente do sistema operacional, que o Python então consegue acessar através do módulo os.

## Como usar ?

- Agora sim, vamos escrever código de verdade. Primeiro, precisamos de um jeito de carregar o ``.env`` e disponibilizar essas variáveis pro resto do código acessar.

O python-dotenv funciona assim: você chama uma ``função load_dotenv()`` (que lê o arquivo .env e "injeta" as variáveis no ambiente), e depois usa ``os.getenv("NOME_DA_CHAVE")`` pra pegar o valor de cada uma.

- Separar ``"como conectar"`` de ``"o que fazer com a conexão"`` também é uma responsabilidade própria.


# variável especial chamada

```
if __name__ == "__main__":
    conexao = conectar()
    print("Conectado com sucesso!")
```

## O problema que isso resolve

Todo módulo Python tem uma variável especial chamada __name__, que o próprio Python preenche automaticamente. O valor dela muda dependendo de como o arquivo foi executado:

Se você rodar o arquivo diretamente (ex: python config.py no terminal), o Python define __name__ = "__main__".
Se esse arquivo for importado por outro arquivo (ex: outro código faz from config import conectar), o Python define __name__ = "config" (o nome do próprio módulo) — não "__main__".

Por que isso importa pro seu caso

Você vai, mais pra frente, importar conectar() dentro do seu Repository (from config import conectar). Se você tivesse escrito conexao = conectar() e print(...) soltos no arquivo (sem o if), isso executaria toda vez que qualquer outro arquivo importasse config.py — mesmo que ninguém quisesse testar conexão naquele momento, só quisesse usar a função.

O if __name__ == "__main__": cria uma zona de código que só roda quando você executa esse arquivo específico diretamente — serve como uma área de teste isolada, que fica "desligada" quando o arquivo é usado como peça de outro código maior.

Faz sentido a diferença entre "rodar o arquivo direto" versus "importar o arquivo de dentro de outro"? Corrige o dbname e adiciona esse bloco de teste no final do config.py, depois roda o arquivo direto no terminal (py src/database/config.py, ajustando o caminho conforme sua estrutura) pra ver se conecta de verdade.

# Como previnir o SQL Injection

- SQL Injection, e é um dos mais conhecidos e perigosos da área.

- Imagina que alguém, em vez de digitar um nome normal, digite isto como "nome da conta":

```
Ikaro'); DROP TABLE conta; --
```

- Se você tivesse usado aquele ``f"INSERT INTO conta (nome) VALUES ('{nome_digitado}')"``, a string final montada seria:

```
INSERT INTO conta (nome) VALUES ('Ikaro'); DROP TABLE conta; --')
```
- Repara: as aspas simples que a pessoa digitou fecham a string antes da hora, e o que vem depois (``DROP TABLE conta``) vira um comando SQL novo e válido, que o banco executa — nesse exemplo, apagando sua tabela inteira. O -- no final comenta o resto, pra evitar erro de sintaxe. Esse é o ataque clássico.

# A solução: parâmetros preparados (prepared statements)

- Em vez de "montar" a query colando texto direto (``f"..."``), o ``psycopg2`` te dá um jeito de passar os valores separados da query, usando ``%s`` como marcador de posição:

```
cursor.execute("INSERT INTO conta (nome) VALUES (%s)", (nome_digitado,))
```

- Aqui, o ``psycopg2`` sabe que tudo que estiver no lugar do ``%s`` é dado, nunca comando — então mesmo que alguém digite aspas ou ``DROP TABLE``, isso é tratado como texto puro, sem nenhum efeito de "quebrar" a query.

# O que é um cursor

- Quando você chama ``conectar()``, você recebe uma conexão com o banco — é como uma "linha telefônica aberta" com o Postgres. Mas só ter a linha aberta não é suficiente pra "falar" com o banco — você precisa de algo que realmente envie comandos e receba respostas através dessa conexão.

- O cursor é exatamente isso: é o objeto que você usa pra executar queries SQL e navegar pelos resultados que voltam (no caso de um SELECT). Pensa nele como o "microfone" daquela ligação — a conexão é o cabo, o cursor é por onde a comunicação de fato acontece.

# Uso na prática

```
conexao = conectar()
cursor = conexao.cursor()

cursor.execute("INSERT INTO conta (nome) VALUES (%s)", (nome,))

conexao.commit()  # confirma a alteração de verdade no banco
cursor.close()
conexao.close()
```

## Alguns pontos importantes

1. ``conexao.cursor()`` cria o cursor a partir da conexão já aberta.
2. ``cursor.execute(...)`` roda a query, com o ``%s`` sendo substituído com segurança pelo valor de ``nome`` (lembra da proteção contra SQL Injection que acabamos de ver).
3. ``conexao.commit()`` é essencial pra INSERT/UPDATE/DELETE — sem isso, o Postgres trata a alteração como "pendente" e ela não fica salva de verdade. (Pra ``SELECT``, não precisa de commit, porque você só está lendo, não alterando nada.)
4. No final, é boa prática fechar o cursor e a conexão, pra não deixar recursos abertos sem necessidade

# Começo do Repository

- Para criarmos a nossa conexão com o banco precisamos criar nossas sequencias de código
- Seguimos os determinados passos para esse processo:

1. Abrir a conexão ``(conectar())``
2. Criar o cursor
3. Executar o ``INSERT INTO conta (nome) VALUES (%s) RETURNING id``, passando o ``nome`` recebido como parâmetro
4. Pegar o ``id`` que voltou do ``RETURNING``
5. Fechar tudo (commit, cursor, conexão)
6. Montar e devolver um objeto ``Conta(id=..., nome=...)``

- Primeiro precisamos da nossa conexão:

```
from database import conectar()

conexao = conectar()
```

- importamos de onde está nossa fução de conexão
- depois colocamos o conecar dentro da função criar_conta

- Depois criamos o cursor logo a seguir 

```
curso = conexao.cursor()
```

- Em seguida dentro da função executamos o comando ``cursor.execute``

```
    cursor.execute("INSERT INTO conta (nome) VALUES (%s) RETURNING id)", (nome,))
```

- Depois criamos o ``fetchone`` para retornar nosso ID

```
    conta_id = cursor.fetchone()[0] 
```

- Depois adicionamos o commit se não as alterações não serão salvas

```
    conexao.commit()
```

- Nós adicionamos os comandos para sair da funão:

```
curso.close()
conexao.close()
```

- E por fim retornamos os dados da conta:

```
return Conta(id=id_gerado, nome=nome)
```

- Lembrando que precisamos importar nosso objeto Conta de Conta_entidadades.py

- Agora vamos testar com uma função de teste!
- Uma forma rápida de testar: adiciona, temporariamente, no final do arquivo (fora da função, sem indentação):

```
if = __name__ == "__main":
    nova_conta = criar_conta("Teste")
    print("Nova Conta")
```

- Depois temos que conferiri se o venv está ativo no terminal
- Se não estiver ativo só rodar o comando novamente para ativar:

```
source .venv/bin/activate
```

# Criando Repository Transação 

- Primeiro importamos a conexão com a função ``conectar()```
- Depois fazemos tambem para importa nossa entidade
- logo após precisamos importar tambem o modulo ``datetime``` para retornarmos a parte da data
- depois precisamos tambem importar o tipo da transação do nosso objeto

- Seguimos tambem nossa sequencia de criação do padrão solido:

```
(conectar → cursor → execute com %s → fetchone → commit → close → devolver objeto de domínio)
```

- Logo depois criamos nosso código padão de testes para testarmos se a criação funcionou

```
if __name__ == "__main__":
    nova_transacao = criar_transacao("Teste", 100.0, 1, date(2024, 8, 26), TipoTransacao.ENTRADA, "Salário")
    print(nova_transacao)
```

- Ela trouxe todos os parâmetros da nossa entidade

## Criando Repository para buscar por ID

- Diferente do ``INSERT`` para inserir um novo valor a tabela para buscar algo usamos o comando sql ``SELECT```

- pra buscar uma conta específica pelo id, você precisa de duas partes na query — quais colunas você quer trazer de volta, e uma condição pra filtrar só a linha certa (não a tabela inteira). Lembra da sintaxe geral:

```
SELECT colunas FROM tabela WHERE condição;
```
- Para retornar por ``id`` e se proteger contra SQL Ijection usaremos o comando da seguinte forma:

```
SELECT * FROM conta WHERE id = %s
```

- ``SELECT *`` traz todas as colunas, e ``WHERE id = %s`` filtra pela conta certa, com o valor sendo passado de forma segura (protegido contra SQL Injection).

- Criando a funcão:

Não precisa de ``commit()``
Lembra que ``commit()`` só é necessário quando você altera dados (``INSERT``, ``UPDATE``, ``DELETE``)? Um ``SELECT`` só lê, não muda nada no banco — então não tem nada pra "confirmar".

2. ``fetchone()`` aqui devolve a linha inteira, não só um valor
Na ``criar_conta``, você usou ``fetchone()[0]`` porque o ``RETURNING id`` só devolvia uma coluna (o id). Aqui, como você pediu ``SELECT *``, o ``fetchone()`` vai devolver uma tupla com todos os valores da linha — algo como ``(1, 'Ikaro')``. Você vai precisar pegar duas posições dessa tupla (``[0]`` pro id, ``[1]`` pro nome), não só uma.

3. E se a conta não existir?
Pensa nisso: se você buscar um ``id`` que não existe no banco, o que ``cursor.fetchone()`` devolve? (dica: quando não há nenhuma linha correspondente, ``fetchone()`` devolve ``None``, não uma tupla vazia). Isso significa que, antes de tentar acessar ``resultado[0]`` e ``resultado[1]``, você precisa verificar se o resultado não é ``None`` — senão, tentar acessar ``None[0]`` vai gerar um erro.

Pensando nisso: se a conta não for encontrada, o que você acha que a função ``buscar_conta_por_id`` deveria fazer — devolver ``None`` (avisando "não achei nada"), ou lançar algum tipo de erro (parecido com o ``ValueError`` que criamos na regra de "valor não pode ser negativo")

### Regra 

```
A regra geral em Python: tudo que uma função usa precisa já estar definido antes de ela ser chamada (não necessariamente antes de ser definida, mas com certeza antes de ser executada).
```

## Criando Repository para buscar por contas

- ``buscar_conta_por_id`` usava ``cursor.fetchone()``, porque só esperava uma linha de resultado (ou nenhuma). Aqui, você espera múltiplas linhas — todas as transações daquela conta.

- ``fetchall()`` funciona parecido com ``fetchone()``, mas em vez de devolver uma tupla (ou None), ele devolve uma lista de tuplas — uma tupla pra cada linha que a query encontrou. Se não encontrar nenhuma linha, ele devolve uma lista vazia (``[]``), não ``None`` — essa é uma diferença importante em relação ao ``fetchone()``.

- Exemplo, se a conta 1 tiver 3 transações, cursor.fetchall() devolveria algo como:

```
[
    (1, 1, 'Salário', 100.0, ..., 'Entrada'),
    (2, 1, 'Lanche', 15.0, ..., 'saida'),
    (3, 1, 'Ônibus', 5.0, ..., 'saida'),
]
```

- em vez de tratar um resultado, você precisa percorrer cada tupla dessa lista e transformar cada uma num objeto ``Transacao``

Busca todas as ``transações de uma conta`` com ``SELECT ... WHERE conta_id = %s``
- Usa ``fetchall()`` em vez de ``fetchone()`` — traz várias linhas de uma vez, numa lista de tuplas (fetchone() só serve pra uma linha ou None)
- Percorre os resultados com um ``for``, montando um ``objeto Transacao`` pra cada linha e adicionando numa lista com ``.append()``
- tipo precisa ser reconstruído do ``Enum``: o banco guarda como string (``"Entrada"``), então a volta é ``TipoTransacao(resultado[6])``
- Testado com sucesso: retornou as 2 transações de teste da conta 1, com todos os campos corretos (incluindo valor já vindo como Decimal)

---

# Rodar como módulo (para imports funcionarem certo)

- Como separei a pasta de teste fora de src, como rodar o arquivo para testar se o calculo das transações está funcionando? 

- Esse arquivo novo está fora de ``src/``, então ele não pode mais usar aqueles imports relativos com ``..`` (que só funcionam dentro de um pacote). Como esse arquivo vai importar ``listar_transacoes_por_conta`` (que mora em ``src/repository/transacao_repository.py``) e ``calcular_saldo`` (em ``src/Domain/conta_regras.py``)?

1. Isso vai exigir um ``import absoluto``, começando a partir de ``src``, tipo:

```
from src.repository.transacao_repository import listar_transacoes_por_conta
from src.Domain.conta_regras import calcular_saldo
```

- Só que pra isso funcionar, o Python precisa executar esse arquivo a partir da raiz do projeto (não de dentro de ``testes/``), do mesmo jeito que fazíamos com ``-m src.repository....`` Como você acha que ficaria o comando pra rodar esse novo arquivo, sabendo que ele mora em ``testes/teste_saldo.py`` e você quer rodar a partir da raiz?

- ``tests/`` é irmã de ``src/``ou seja elas estão no mesmo nível de estrutura, então o caminho do módulo deveria começar direto por ``testes``, sem passar por src

```
python3 -m testes.teste_saldo
```

- Isso, combinado com o import absoluto que você vai escrever dentro do arquivo (``from src.repository... import ...``), reflete a estrutura real: a partir da raiz do projeto, existem duas pastas irmãs, ``src/`` e ``testes/``, e o Python "enxerga" as duas quando você roda o comando de dentro da raiz.

# Montar o teste_saldo.py

- Meu raciocínio:

1. Buscar as transações de uma conta que já existe (você tem a conta 1, que já tem 2 transações de teste)
2. Passar essa lista pro calcular_saldo
3. Imprimir o resultado, pra você conferir se bate com o que você espera manualmente

# Pytest

- Para podermos testar se a função de ``testar_saldo``está funcionando podemos usar uma ferramenta no python chamada ``pytest```

- ``pytest`` é uma ferramenta de testes pra Python — provavelmente a mais usada do mercado. A ideia central dela é simples: em vez de você escrever manualmente "roda essa função, confere se deu certo, imprime alguma coisa se falhar", o ``pytest`` faz isso tudo por você, de forma padronizada.

## Como funciona na prática:

1. Qualquer função cujo nome comece com test_ (exatamente como você já nomeou a sua, test_calcular_saldo) é automaticamente reconhecida como um teste.
2. Você não precisa de if __name__ == "__main__": nem chamar a função manualmente — o pytest varre os arquivos, encontra as funções test_*, e executa todas.
3. Quando um assert dentro do teste falha, o pytest te mostra uma mensagem bem detalhada: qual valor era esperado, qual valor realmente veio, e em que linha — muito mais claro que um erro genérico de AssertionError.
4. Se tudo passar, ele mostra um resumo verde, tipo "1 passed".

## Como se usa:

Instala com ``pip install pytest`` (mais uma linha no seu requirements.txt)
Roda no terminal, na raiz do projeto: ``pytest`` (sozinho, sem precisar apontar arquivo nenhum — ele encontra os testes automaticamente)

- Por que isso ``importa pro seu projeto``: conforme você for adicionando mais ``regras de negócio (validação de valor negativo, cálculo de saldo, futuras regras)``, você vai acumular vários testes. Rodar todos eles de uma vez com um comando só ``(pytest)``, em vez de executar arquivo por arquivo manualmente, economiza bastante tempo — e vira um hábito valioso pra qualquer projeto sério, incluindo os que você vai construir pensando numa vaga de desenvolvedor.

- Começamos instalando ele pelo terminal, lembrar do ``.venv`` ativo no termina!

```
pip install pytest
or
python3 -m pip install pytest
```

- Depois de instalado, atualiza o ``requirements.txt``

```
pip freeze > requirements.txt
or 
python3 -m pip freeze > requirements.txt
```

- Com isso feito, você não precisa mais do ``if __name__ == "__main__"``: nesse arquivo — o ``pytest`` vai descobrir a função ``test_calcular_saldo`` sozinho, só pelo nome dela. Pode deixar o arquivo só com os dois imports e a função `test_calcular_saldo()`, sem nenhum bloco de execução manual.

- Ai só rodar o pytest a partir da raiz do projeto:

```
pytest
```
- você não usa ``-m`` nem precisa apontar o caminho do arquivo — o ``pytest`` varre o projeto inteiro procurando por arquivos e funções de teste automaticamente

- o pytest `"descobre"` arquivos de teste — ele não varre qualquer arquivo `.py`, ele procura por um padrão de nome.

- Por padrão, o `pytest` só reconhece arquivos que começam com `test_` ou terminam com `_test.py`.

# O que é FastAPI

- É um framework Python pra criar APIs web — ou seja, o código que fica "escutando" na internet (ou na sua máquina) esperando requisições HTTP, e respondendo com dados (geralmente em JSON).

- Pensa numa analogia com o que você já construiu: o Repository é como um "balcão de atendimento interno" — só o próprio código Python consegue chamar `criar_conta(nome)`. A API é como abrir uddizesse balcão pro mundo externo — agora alguém usando um navegador, um app de celular, ou uma ferramenta como Postman/Insomnia consegue mandar uma requisição HTTP e receber uma resposta, sem precisar saber Python nem importar nada.

# Os conceitos centrais que você vai usar:

- `Rota (endpoint)`— uma URL que responde a um tipo de requisição, tipo `POST /contas` (criar conta) ou `GET /contas/1` (buscar conta com id 1).

- `Verbo HTTP` — cada rota tem uma "ação" associada: `GET (buscar/ler)`, `POST (criar)`, `PUT/PATCH (atualizar)`, `DELETE (remover)`. Você já tem funções que mapeiam quase direto pra esses verbos: criar_conta → POST, buscar_conta_por_id → GET.
- `JSON` — o formato que a API usa pra `"conversar"` com quem fizer a requisição (tanto pra receber dados quanto pra devolver).

- Criar conta seria um POST,  consultar saldo é um GET,  Registrar transação seria um POST e ver historico seria um GET

Um padrão bem comum em `APIs REST` é organizar as rotas em torno dos recursos `(as entidades: contas, transacoes)`, assim:

```
Criar conta → POST /contas
Registrar transação → POST /transacoes
Consultar saldo → GET /contas/{id}/saldo (o saldo é "de uma conta específica", por isso o id aparece na URL)
Ver histórico → GET /contas/{id}/transacoes (histórico também é "de uma conta específica")
```
- Repara no padrão `{id}` — isso se chama parâmetro de rota `(path parameter)`: é uma parte variável da URL, que o FastAPI extrai automaticamente e entrega pra sua função como se fosse um argumento comum.

- O FastAPI, sozinho, só define como construir a API — mas pra ela realmente "rodar" e "escutar" requisições, você precisa de um servidor por baixo. O mais comum, e que a documentação oficial do FastAPI recomenda, é o uvicorn. Instala ele também

## O que o __init__.py faz

- Como vamos utilizar ele novamente, Ele é um arquivo (geralmente vazio, ou quase) que marca uma pasta como um `pacote Python`. Sem ele, o Python trata a pasta só como `"uma pasta comum"` — e não consegue fazer certos tipos de `import relativo` (aqueles com `.` ou `..`) de dentro dela nem através dela.

