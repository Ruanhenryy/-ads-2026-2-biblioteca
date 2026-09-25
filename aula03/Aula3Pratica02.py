preco = float(input("Preço unitário: "))
qtd = int(input("Quantidade: "))
total = preco * qtd
com_desconto = total * 0.9
print(total)
print(f"Total: R$ {com_desconto:.2f}")