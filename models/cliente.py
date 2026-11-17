from models.pessoa import Pessoa


class Cliente(Pessoa):
    """Representa um cliente da livraria.

    Cliente herda de Pessoa, portanto já recebe nome, CPF, telefone e e-mail.
    Além desses dados, mantém uma lista de compras associadas ao objeto.
    """

    def __init__(self, nome, cpf, telefone="", email=""):
        # super() chama o construtor da classe Pessoa.
        super().__init__(nome, cpf, telefone, email)
        self.historico_compras = []

    def adicionar_compra(self, compra):
        """Adiciona uma compra à lista de histórico deste cliente."""
        self.historico_compras.append(compra)

    def consultar_historico(self):
        """Devolve uma cópia da lista para não expor a lista interna diretamente."""
        return list(self.historico_compras)
