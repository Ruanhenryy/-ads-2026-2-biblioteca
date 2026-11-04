from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from services.livraria import Livraria


class LivroCadastro(BaseModel):
    isbn: str = Field(min_length=1)
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    preco: float = Field(ge=0)
    estoque: int = Field(ge=0)


class ClienteCadastro(BaseModel):
    nome: str = Field(min_length=1)
    cpf: str = Field(min_length=1)
    telefone: str = ""
    email: str = ""

class FuncionarioCadastro(BaseModel):
    nome : str = Field(min_length=1)
    cpf : str = Field(min_length=1)
    telefone: str = Field(min_length=1)
    email : str = Field(min_length=1)
    matricula: str = Field(min_length=1)
    cargo : str = Field(min_length=1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.livraria = Livraria()
    try:
        yield
    finally:
        app.state.livraria.fechar()


app = FastAPI(title="Biblioteca de Bairro", lifespan=lifespan)


@app.get("/livros/listar")
async def listar_livros(request: Request):
    return request.app.state.livraria.listar_livros()


@app.post("/livros/cadastrar")
async def cadastrar_livro(livro: LivroCadastro, request: Request):
    try:
        livro_id = request.app.state.livraria.cadastrar_livro(
            livro.isbn,
            livro.titulo,
            livro.autor,
            livro.preco,
            livro.estoque
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    return {"mensagem": "Livro cadastrado com sucesso.", "id": livro_id}


@app.post("/cliente/cadastrar")
async def cadastrar_cliente(cliente: ClienteCadastro, request: Request):
    try:
        cliente_id = request.app.state.livraria.cadastrar_cliente(
            cliente.nome,
            cliente.cpf,
            cliente.telefone,
            cliente.email
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    return {"mensagem": "Cliente cadastrado com sucesso.", "id": cliente_id}


@app.post("/funcionario/cadastrar")
async def cadastrar_funcionario(funcionario: FuncionarioCadastro,  request: Request):
        try:
            funcionario_id = request.app.state.livraria.cadastrar_funcionario(
                funcionario.nome,
                funcionario.cpf,
                funcionario.telefone,
                funcionario.email,
                funcionario.matricula,
                funcionario.cargo
            )
        except ValueError as erro:
            raise HTTPException(status_code=400, detail=str(erro)) from erro
        return {"mensagem": "Funcionario cadastrado com sucesso.", "id": funcionario_id}