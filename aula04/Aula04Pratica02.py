from decimal import Decimal

precos = {
    "Emprestimo": Decimal("5.00"),
    "Renovacao": Decimal("3.00"),
    "Multa": Decimal("2.00"),
}

def itens_validos(comanda):
    return [item for item in comanda if item in precos]


def subtotal(comanda):
    return sum((precos[item] for item in itens_validos(comanda)), Decimal("0.00"))


def desconto(comanda, valor):
    itens = itens_validos(comanda)

    if len(itens) >= 3:
        return valor * Decimal("0.10")

    return Decimal("0.00")


def fechar(comanda):
    itens = itens_validos(comanda)
    valor_subtotal = subtotal(itens)
    valor_desconto = desconto(itens, valor_subtotal)
    total = valor_subtotal - valor_desconto

    return {
        "subtotal": valor_subtotal,
        "desconto": valor_desconto,
        "total": total
    }


comanda = ["Emprestimo", "Renovacao", "Emprestimo", "Livro inexistente"]

resultado = fechar(comanda)

print(f"Subtotal: R$ {resultado['subtotal']:.2f}")
print(f"Desconto: R$ {resultado['desconto']:.2f}")
print(f"Total: R$ {resultado['total']:.2f}")