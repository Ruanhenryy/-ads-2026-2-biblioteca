"""Ponto de entrada da API do Sistema de Livraria.

Este arquivo transforma as operações que já existem na classe Livraria
em endpoints HTTP. As regras de negócio continuam em services/livraria.py.
"""

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

from services.livraria import Livraria


# ---------------------------------------------------------------------------
# MODELOS DE ENTRADA (SCHEMAS)
# ---------------------------------------------------------------------------
# As classes abaixo definem quais dados a API espera receber em cada JSON.
# O FastAPI usa o Pydantic para validar esses dados automaticamente.


class LivroCadastro(BaseModel):
    """Dados necessários para cadastrar um livro."""

    isbn: str = Field(min_length=1, description="ISBN ou código único do livro")
    titulo: str = Field(min_length=1, description="Título do livro")
    autor: str = Field(min_length=1, description="Nome do autor")
    preco: float = Field(ge=0, description="Preço; não pode ser negativo")
    estoque: int = Field(ge=0, description="Quantidade inicial em estoque")


class ClienteCadastro(BaseModel):
    """Dados necessários para cadastrar um cliente."""

    nome: str = Field(min_length=1)
    cpf: str = Field(min_length=1)
    # Telefone e e-mail são opcionais na lógica original.
    telefone: str = ""
    email: str = ""


class FuncionarioCadastro(BaseModel):
    """Dados necessários para cadastrar um funcionário."""

    nome: str = Field(min_length=1)
    cpf: str = Field(min_length=1)
    telefone: str = Field(min_length=1)
    email: str = Field(min_length=1)
    matricula: str = Field(min_length=1)
    cargo: str = Field(min_length=1)


class ItemCompra(BaseModel):
    """Representa um livro e a quantidade comprada."""

    livro_id: int = Field(gt=0, description="ID do livro cadastrado")
    quantidade: int = Field(gt=0, description="Quantidade maior que zero")


class CompraCadastro(BaseModel):
    """Dados necessários para registrar uma compra."""

    cliente_id: int = Field(gt=0, description="ID do cliente")
    funcionario_id: int = Field(gt=0, description="ID do funcionário")
    # min_length=1 impede que uma compra seja enviada sem nenhum livro.
    itens: list[ItemCompra] = Field(min_length=1)


# ---------------------------------------------------------------------------
# CONEXÃO COM A CAMADA DE REGRAS DE NEGÓCIO
# ---------------------------------------------------------------------------


def obter_livraria():
    """Cria uma conexão para atender à requisição atual.

    A conexão é fechada ao final da requisição, inclusive quando acontece
    algum erro. Assim, não deixamos uma conexão SQLite aberta sem necessidade.
    """

    livraria = Livraria()
    try:
        yield livraria
    finally:
        livraria.fechar()


def transformar_erro(erro: ValueError) -> HTTPException:
    """Converte erros da camada de negócio em respostas HTTP.

    A classe Livraria informa problemas usando ValueError. A API converte
    esses problemas para HTTP 400 (dados/operação inválidos) ou HTTP 404
    (registro que não foi encontrado).
    """

    mensagem = str(erro)

    if "não encontrado" in mensagem.lower():
        codigo_http = 404
    else:
        codigo_http = 400

    return HTTPException(status_code=codigo_http, detail=mensagem)


# A documentação automática ficará disponível em /docs.
app = FastAPI(
    title="Sistema de Livraria",
    description=(
        "API para cadastro de clientes, funcionários e livros, "
        "controle de estoque, registro de compras e histórico de clientes."
    ),
    version="1.0.0",
)


@app.get("/", tags=["Início"])
def inicio():
    """Mostra uma mensagem inicial e indica onde testar a API."""

    return {
        "mensagem": "API do Sistema de Livraria em funcionamento!",
        "documentacao": "/docs",
    }


# ---------------------------------------------------------------------------
# LIVROS
# ---------------------------------------------------------------------------


@app.get("/livros/listar", tags=["Livros"])
def listar_livros(livraria: Livraria = Depends(obter_livraria)):
    """Lista todos os livros e mostra também o estoque atual."""

    return livraria.listar_livros()


@app.post("/livros/cadastrar", status_code=201, tags=["Livros"])
def cadastrar_livro(
    livro: LivroCadastro,
    livraria: Livraria = Depends(obter_livraria),
):
    """Recebe os dados de um livro e chama o método original de cadastro."""

    try:
        livro_id = livraria.cadastrar_livro(
            livro.isbn,
            livro.titulo,
            livro.autor,
            livro.preco,
            livro.estoque,
        )
    except ValueError as erro:
        raise transformar_erro(erro) from erro

    return {
        "mensagem": "Livro cadastrado com sucesso.",
        "id": livro_id,
    }


@app.get("/livros/pesquisar", tags=["Livros"])
def pesquisar_livros(
    termo: str = Query(min_length=1, description="Título, autor ou ISBN"),
    livraria: Livraria = Depends(obter_livraria),
):
    """Pesquisa livros por parte do título, do autor ou do ISBN."""

    # Evita que uma pesquisa formada apenas por espaços seja tratada como %%
    # pelo comando LIKE e acabe retornando todos os livros.
    if not termo.strip():
        raise HTTPException(status_code=400, detail="Informe um termo para pesquisar.")

    return livraria.buscar_livros(termo)


# ---------------------------------------------------------------------------
# CLIENTES
# ---------------------------------------------------------------------------


@app.post("/cliente/cadastrar", status_code=201, tags=["Clientes"])
def cadastrar_cliente(
    cliente: ClienteCadastro,
    livraria: Livraria = Depends(obter_livraria),
):
    """Cadastra um cliente usando o método já existente em Livraria."""

    try:
        cliente_id = livraria.cadastrar_cliente(
            cliente.nome,
            cliente.cpf,
            cliente.telefone,
            cliente.email,
        )
    except ValueError as erro:
        raise transformar_erro(erro) from erro

    return {
        "mensagem": "Cliente cadastrado com sucesso.",
        "id": cliente_id,
    }


@app.get("/clientes/listar", tags=["Clientes"])
def listar_clientes(livraria: Livraria = Depends(obter_livraria)):
    """Lista os clientes cadastrados."""

    return livraria.listar_clientes()


@app.get("/cliente/{cliente_id}/historico", tags=["Clientes", "Compras"])
def historico_cliente(
    cliente_id: int = Path(gt=0, description="ID do cliente"),
    livraria: Livraria = Depends(obter_livraria),
):
    """Mostra as compras de um cliente, incluindo os itens de cada compra."""

    try:
        return livraria.historico_cliente(cliente_id)
    except ValueError as erro:
        raise transformar_erro(erro) from erro


# ---------------------------------------------------------------------------
# FUNCIONÁRIOS
# ---------------------------------------------------------------------------


@app.post("/funcionario/cadastrar", status_code=201, tags=["Funcionários"])
def cadastrar_funcionario(
    funcionario: FuncionarioCadastro,
    livraria: Livraria = Depends(obter_livraria),
):
    """Cadastra um funcionário."""

    try:
        funcionario_id = livraria.cadastrar_funcionario(
            funcionario.nome,
            funcionario.cpf,
            funcionario.telefone,
            funcionario.email,
            funcionario.matricula,
            funcionario.cargo,
        )
    except ValueError as erro:
        raise transformar_erro(erro) from erro

    return {
        "mensagem": "Funcionário cadastrado com sucesso.",
        "id": funcionario_id,
    }


@app.get("/funcionarios/listar", tags=["Funcionários"])
def listar_funcionarios(livraria: Livraria = Depends(obter_livraria)):
    """Lista os funcionários cadastrados."""

    return livraria.listar_funcionarios()


# ---------------------------------------------------------------------------
# COMPRAS
# ---------------------------------------------------------------------------


@app.post("/compras/registrar", status_code=201, tags=["Compras"])
def registrar_compra(
    compra: CompraCadastro,
    livraria: Livraria = Depends(obter_livraria),
):
    """Registra uma compra e solicita a baixa automática do estoque.

    A API converte os itens recebidos em uma lista de tuplas porque esse é
    o formato esperado pelo método registrar_compra() da classe Livraria.
    Toda a validação e a transação continuam sendo feitas nesse método.
    """

    itens = [
        (item.livro_id, item.quantidade)
        for item in compra.itens
    ]

    try:
        compra_id, total = livraria.registrar_compra(
            compra.cliente_id,
            compra.funcionario_id,
            itens,
        )
    except ValueError as erro:
        raise transformar_erro(erro) from erro

    return {
        "mensagem": "Compra registrada com sucesso.",
        "compra_id": compra_id,
        "total": total,
    }
