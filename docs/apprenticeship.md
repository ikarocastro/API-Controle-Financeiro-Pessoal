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