# Sistema de Livraria — Python, POO e SQLite

Projeto de terminal para cadastro de clientes e funcionários, controle de livros em estoque, registro de vendas e histórico de compras.

## Requisitos

- Python 3.10 ou superior recomendado.
- Não é necessário instalar dependências externas: o projeto usa `sqlite3`, que acompanha o Python.

## Como executar

1. Extraia o arquivo ZIP.
2. Abra o terminal na pasta `sistema_livraria`.
3. Execute:

   ```bash
   python main.py
   ```

   Em algumas instalações Linux, pode ser necessário usar `python3 main.py`.

4. O banco `database/livraria.db` será criado automaticamente na primeira execução.

## Ordem sugerida para testar

1. Cadastre um cliente.
2. Cadastre um funcionário.
3. Cadastre um livro com estoque maior que zero.
4. Registre uma compra usando os IDs apresentados pelo sistema.
5. Consulte o estoque para confirmar a baixa.
6. Consulte o histórico do cliente.

## Estrutura

- `models/`: classes que representam Pessoa, Cliente, Funcionário, Livro e Compra.
- `services/livraria.py`: regras de negócio e acesso ao SQLite.
- `main.py`: menu e interação com o usuário.
- `database/`: arquivo do banco de dados criado durante a execução.

## Conceitos de POO e banco de dados

- Herança: `Cliente` e `Funcionario` herdam de `Pessoa`.
- Encapsulamento de responsabilidades: modelos, regras de negócio e interface estão separados.
- Objetos e métodos.
- Relacionamentos entre clientes, funcionários, compras e livros.
- SQLite com chaves primárias, chaves estrangeiras e restrições de unicidade.
- Transação atômica para registrar uma compra e baixar o estoque: se uma validação falhar, a operação é desfeita.

## Observações

- O CPF é armazenado como texto para preservar zeros à esquerda.
- O ISBN/código do livro precisa ser único.
- O projeto é uma versão acadêmica inicial. Antes de usar em produção, acrescente autenticação, autorização, validação mais completa de CPF/e-mail, testes automatizados e rotinas de backup.


## Equipe

- Ruan Henry (@Ruanhenryy)
- Breno Mesquita (@Brenotxt)
- Benvenuto Estevão (@estevo007)
- Joao Pedro Mesquita (@JPML31)
- José luiz (@JoseLuiz-senac)