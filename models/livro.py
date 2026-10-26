class Livro:
    """Representa um livro e seu estoque."""

    def __init__(self, isbn, titulo, autor, preco, estoque=0):
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        if estoque < 0:
            raise ValueError("O estoque não pode ser negativo.")
        self.isbn = isbn.strip()
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.preco = float(preco)
        self.estoque = int(estoque)

    def consultar_disponibilidade(self):
        return self.estoque > 0

    def atualizar_estoque(self, quantidade):
        """Quantidade positiva adiciona unidades; negativa remove."""
        if self.estoque + quantidade < 0:
            raise ValueError("Estoque insuficiente.")
        self.estoque += quantidade
