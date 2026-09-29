class Comanda:
    def __init__(self, itens):
        if not isinstance(itens, list):
            raise ValueError("Os itens devem ser uma lista")

        self.itens = itens

    def itens_validos(self):
        precos = {
            "Emprestimo": 5.00,
            "Renovacao": 3.00,
            "Multa": 2.00
        }

        return [item for item in self.itens if item in precos]

    def subtotal(self):
        precos = {
            "Emprestimo": 5.00,
            "Renovacao": 3.00,
            "Multa": 2.00
        }

        return sum(precos[item] for item in self.itens_validos())