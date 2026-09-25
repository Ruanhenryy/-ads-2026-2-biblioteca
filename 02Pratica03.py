valor = float(input("Valor da compra:"))
cupom = input("tem cupom? (s/n) ").lower() == "s"

if cupom or valor > 300:
    frete = 0.0
elif valor >= 100:
    frete = 8.0
else:
    frete = 15.0

print(f"Frete: R$ {frete:.2f}")
print(f"Total: R$ {valor + frete:.2f}")        