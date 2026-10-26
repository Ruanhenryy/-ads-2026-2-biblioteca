from models.pessoa import Pessoa


class Cliente(Pessoa):
    """Representa um cliente da livraria."""

    def __init__(self, nome, cpf, telefone="", email=""):
        super().__init__(nome, cpf, telefone, email)
        self.historico_compras = []

    def adicionar_compra(self, compra):
        self.historico_compras.append(compra)

    def consultar_historico(self):
        return list(self.historico_compras)
