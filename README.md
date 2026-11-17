# Sistema de Livraria — API com FastAPI e SQLite

Projeto acadêmico de ADS baseado na lógica original do Sistema de Livraria.
A aplicação mantém o menu de terminal em `main.py` e disponibiliza uma API HTTP
em `mainApi.py`. As regras de cadastro, pesquisa, compra e estoque continuam
centralizadas na classe `Livraria`, localizada em `services/livraria.py`.

## 1. Requisitos

- Python 3.10 ou superior.
- FastAPI e Uvicorn (instalados pelo `requirements.txt`).
- SQLite, que já acompanha o Python.

## 2. Instalação

Abra o terminal na pasta do projeto e execute:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 3. Executar a API

Na pasta onde está `mainApi.py`, execute:

```bash
uvicorn mainApi:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.
A documentação interativa do Swagger ficará em:

`http://127.0.0.1:8000/docs`

O banco utilizado é `database/livraria.db`. Se o arquivo ainda não existir,
a classe `Livraria` cria a pasta e as tabelas automaticamente na primeira
requisição. O arquivo de banco que já acompanha este projeto foi mantido.

## 4. Endpoints disponíveis

| Método | Caminho | O que faz |
|---|---|---|
| GET | `/` | Confirma que a API está funcionando |
| POST | `/cliente/cadastrar` | Cadastra cliente |
| GET | `/clientes/listar` | Lista clientes |
| POST | `/funcionario/cadastrar` | Cadastra funcionário |
| GET | `/funcionarios/listar` | Lista funcionários |
| POST | `/livros/cadastrar` | Cadastra livro |
| GET | `/livros/listar` | Lista livros e estoque |
| GET | `/livros/pesquisar?termo=python` | Pesquisa título, autor ou ISBN |
| POST | `/compras/registrar` | Registra compra e baixa estoque |
| GET | `/cliente/1/historico` | Consulta histórico do cliente de ID 1 |

Os endpoints de cadastro respondem com HTTP 201 quando o registro é criado.
Erros de validação retornam uma resposta HTTP adequada, com a explicação no
campo `detail`.

## 5. Exemplos de dados para enviar pelo Swagger

### Cadastrar cliente — `POST /cliente/cadastrar`

```json
{
  "nome": "Maria Silva",
  "cpf": "12345678900",
  "telefone": "81999999999",
  "email": "maria@email.com"
}
```

### Cadastrar funcionário — `POST /funcionario/cadastrar`

```json
{
  "nome": "João Souza",
  "cpf": "98765432100",
  "telefone": "81988888888",
  "email": "joao@email.com",
  "matricula": "F001",
  "cargo": "Atendente"
}
```

### Cadastrar livro — `POST /livros/cadastrar`

```json
{
  "isbn": "9780000000001",
  "titulo": "Introdução à Programação",
  "autor": "Ana Lima",
  "preco": 59.90,
  "estoque": 10
}
```

### Registrar compra — `POST /compras/registrar`

Os IDs precisam existir no banco. Neste exemplo, cliente e funcionário têm ID 1.
A lista `itens` pode conter um ou vários livros.

```json
{
  "cliente_id": 1,
  "funcionario_id": 1,
  "itens": [
    {
      "livro_id": 1,
      "quantidade": 2
    },
    {
      "livro_id": 2,
      "quantidade": 1
    }
  ]
}
```

## 6. Como a compra funciona

1. A API valida a estrutura do JSON recebido.
2. `mainApi.py` transforma a lista de itens em tuplas, que é o formato usado
   pelo método original `Livraria.registrar_compra()`.
3. O método verifica se cliente e funcionário existem.
4. Verifica se cada livro existe e se há estoque suficiente.
5. Calcula o total e registra a compra e seus itens.
6. Desconta as quantidades compradas do estoque.
7. Todas essas operações acontecem dentro de uma transação SQLite. Se uma
   validação falhar ou ocorrer um erro durante a gravação, as alterações são
   desfeitas.

## 7. Estrutura do projeto

```text
sistema_livraria_api_comentado/
├── database/
│   └── livraria.db
├── models/
│   ├── pessoa.py
│   ├── cliente.py
│   ├── funcionario.py
│   ├── livro.py
│   └── compra.py
├── services/
│   └── livraria.py
├── validation/
│   └── validacoes.py
├── main.py             # Sistema original pelo terminal
├── mainApi.py          # Endpoints da API FastAPI
└── requirements.txt
```

## 8. Entendendo a organização

- `models/`: classes que representam as entidades do projeto. `Cliente` e
  `Funcionario` herdam de `Pessoa`.
- `services/livraria.py`: concentra as regras de negócio e os comandos SQL.
  A API chama os métodos dessa classe em vez de repetir as consultas SQL.
- `mainApi.py`: recebe as requisições HTTP, valida os dados com Pydantic e
  chama os métodos da classe `Livraria`.
- `main.py`: mantém o menu de terminal que já existia no projeto.
- `database/`: guarda o arquivo SQLite.

## 9. O que foi mantido e o que não foi criado

Foram mantidas as operações existentes na lógica original: cadastrar e listar
clientes, funcionários e livros; pesquisar livros; registrar compras; consultar
histórico; e atualizar o estoque durante a compra.

O projeto original não possui regras de negócio para editar ou excluir clientes,
funcionários, livros ou compras. Por isso, esses endpoints não foram inventados.
Podem ser acrescentados depois, quando forem definidas as regras dessas ações.

## 10. Observações acadêmicas

- O CPF permanece como texto para não perder zeros à esquerda.
- O ISBN/código do livro é único.
- A matrícula do funcionário é única.
- O estoque e os preços não podem ser negativos.
- A quantidade de um item de compra precisa ser maior que zero.
- A API ainda não possui autenticação e autorização, como indicado no README
  original. Também não substitui testes automatizados ou rotina de backup.
