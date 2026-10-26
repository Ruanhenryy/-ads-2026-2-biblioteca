from datetime import datetime


class Compra:
    """Representa uma compra com itens, cliente e funcionário."""

    def __init__(self, cliente_id, funcionario_id, itens, compra_id=None, data=None):
        self.id = compra_id
        self.cliente_id = cliente_id
        self.funcionario_id = funcionario_id
        self.itens = itens
        self.data = data or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calcular_total(self):
        return sum(item["preco_unitario"] * item["quantidade"] for item in self.itens)
