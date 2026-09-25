from decimal import Decimal

catalogo = {
    "Hambúrguer": Decimal("25.00"),
    "Pizza": Decimal("40.00"),
    "Batata Frita": Decimal("15.00"),
    "Lasanha": Decimal("30.00"),
    "Refrigerante": Decimal("8.00")
}


# 0 - Retorna apenas os itens válidos
def itens_validos(comanda):
    validos = []

    for item in comanda:
        if item in catalogo:
            validos.append(item)

    return validos


# 1 - Soma apenas os itens válidos
def subtotal(comanda):
    total = Decimal("0.00")

    for item in itens_validos(comanda):
        total += catalogo[item]

    return total


# 2 - Calcula o desconto
def desconto(comanda, valor):
    # A regra do desconto deve ser a da sua equipe
    # Exemplo:
    if valor >= Decimal("100.00"):
        return valor * Decimal("0.10")

    return Decimal("0.00")


# 3 - Fecha a comanda
def fechar(comanda):
    itens = itens_validos(comanda)
    sub = subtotal(comanda)
    desc = desconto(itens, sub)
    total = sub - desc

    return {
        "subtotal": sub,
        "desconto": desc,
        "total": total
    }


# Quem chama é que imprime
comanda = [
    "Hambúrguer",
    "Pizza",
    "Sushi",
    "Batata Frita"
]

resultado = fechar(comanda)

print("Subtotal:", resultado["subtotal"])
print("Desconto:", resultado["desconto"])
print("Total:", resultado["total"])