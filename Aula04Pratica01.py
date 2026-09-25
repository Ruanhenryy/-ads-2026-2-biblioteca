cardapio = ["Hambúrguer", "Pizza", "Batata Frita", "Lasanha", "Refrigerante"]

print("0 - Cardápio:")
for prato in cardapio:
    print(prato)


print("\n1 - Cardápio numerado:")
for numero, prato in enumerate(cardapio, start=1):
    print(numero, "-", prato)


print("\n2 - Total da comanda:")

comanda = [25.00, 40.00, 15.00, 30.00]

total = 0

for preco in comanda:
    total += preco

print("Total: R$", total)


print("\n3 - Quantos pratos cabem em R$ 200?")

dinheiro = 200
preco_prato = 25
quantidade = 0

while dinheiro >= preco_prato:
    dinheiro -= preco_prato
    quantidade += 1

print("Cabem", quantidade, "pratos de R$ 25,00 em R$ 200.")



print("\n4 - Itens da comanda que estão no catálogo:")

comanda_itens = [
    "Hambúrguer",
    "Pizza",
    "Sushi",
    "Batata Frita",
    "Lasanha",
    "Tacos"
]

for item in comanda_itens:
    if item not in cardapio:
        continue

    print(item)