from services.livraria import Livraria
from fastapi import FastAPI

app = FastAPI(title="Loja de Roupas")
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
        print(f"Não foi possível cadastrar: {erro}")