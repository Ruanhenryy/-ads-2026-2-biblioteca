class Livro:
    """Representa um livro e a quantidade disponível em estoque."""

    def __init__(self, isbn, titulo, autor, preco, estoque=0):
        # Essas validações também protegem o objeto quando ele é criado
        # diretamente pelo código Python, sem passar pela API.
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
        """Informa se existe pelo menos uma unidade disponível."""
        return self.estoque > 0

    def atualizar_estoque(self, quantidade):
        """Atualiza o estoque.

        Uma quantidade positiva adiciona unidades; uma quantidade negativa
        remove unidades. A operação é bloqueada caso o estoque fique negativo.
        """
        if self.estoque + quantidade < 0:
            raise ValueError("Estoque insuficiente.")
        self.estoque += quantidade
