servicos = [
    "Emprestimo de livro",
    "Devolucao de livro",
    "Cadastro de socio",
    "Renovacao de livro"
]

for servico in servicos:
    print(servico)

for numero, servico in enumerate(servicos, start=1):
    print(numero, servico)

# 2 - Somar os preços de uma comanda
catalogo = {
    "Emprestimo": 5.00,
    "Renovacao": 3.00,
    "Multa": 2.00
}

comanda = ["Emprestimo", "Renovacao", "Emprestimo"]

total = 0

for item in comanda:
    total += catalogo[item]

print(f"Total da comanda: R$ {total:.2f}")

preco_emprestimo = 5.00
dinheiro = 200
quantidade = 0

while dinheiro >= preco_emprestimo:
    dinheiro -= preco_emprestimo
    quantidade += 1

print(f"Cabem {quantidade} empréstimos em R$ 200.")

comanda = ["Emprestimo", "Renovacao", "Livro Perdido", "Multa"]

for item in comanda:
    if item not in catalogo:
        continue

    print(f"Item válido: {item}")