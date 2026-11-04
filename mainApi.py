from services.livraria import Livraria
from validation.validacoes import pedir_texto, pedir_float, pedir_int
from fastapi import FastAPI

app = FastAPI(title="Biblioteca de Bairro")
livraria = Livraria()


@app.get("/livros/listar")
def listar_livros():
    livros = livraria.listar_livros()
    if not livros:
        return "Nenhum livro cadastrado."
    print("\n--- ESTOQUE DE LIVROS ---")
    for livro in livros:
       return f"ID: {livro['id']} | ISBN: {livro['isbn']} | "f"{livro['titulo']} — {livro['autor']} | "f"R$ {livro['preco']:.2f} | Estoque: {livro['estoque']}"
        

@app.post("/livros/cadastrar")
def cadastrar_livro():
    print("\n--- CADASTRAR LIVRO ---")
    try:
        livro_id = livraria.cadastrar_livro(
            pedir_texto("ISBN/código único: "),
            pedir_texto("Título: "),
            pedir_texto("Autor: "),
            pedir_float("Preço (R$): "),
            pedir_int("Quantidade inicial em estoque: ", minimo=0)
        )
        return f"Livro cadastrado com sucesso! ID: {livro_id}"
    except ValueError as erro:
        return(f"Não foi possível cadastrar: {erro}")

@app.post("/cliente/cadastrar")
def cadastrar_cliente():
    print("\n--- CADASTRAR CLIENTE ---")
    try:
        cliente_id = livraria.cadastrar_cliente(
            pedir_texto("Nome: "),
            pedir_texto("CPF: "),
            input("Telefone: ").strip(),
            input("E-mail: ").strip()
        )
        return(f"Cliente cadastrado com sucesso! ID: {cliente_id}")
    except ValueError as erro:
        return(f"Não foi possível cadastrar: {erro}")