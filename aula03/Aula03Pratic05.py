from decimal import Decimal

precos = {
    "Dom Casmurro": Decimal("5.00"),
    "O Pequeno Principe": Decimal("4.00"),
    "Harry Potter": Decimal("6.00"),
    "Codigo Limpo": Decimal("7.00")
}

comanda = [
    "Dom Casmurro",
    "O Pequeno Principe",
    "Dom Casmurro",
    "Harry Potter",
    "Livro Inexistente"
]

subtotal = Decimal("0.00")
itens_validos = []

for livro in comanda:
    if livro not in precos:
        print(f"Livro não encontrado: {livro}")
        continue

    subtotal += precos[livro]
    itens_validos.append(livro)

quantidade = len(itens_validos)
itens_distintos = len(set(itens_validos))

if quantidade >= 3:
    desconto = subtotal * Decimal("0.10")
else:
    desconto = Decimal("0.00")

total = subtotal - desconto

print(f"\nQuantidade de empréstimos: {quantidade}")
print(f"Livros distintos: {itens_distintos}")
print(f"Subtotal: R$ {subtotal:.2f}")
print(f"Desconto: R$ {desconto:.2f}")
print(f"Total: R$ {total:.2f}")

