"""Funções simples para validar entradas digitadas no menu de terminal.

Essas funções são usadas pelo main.py. Na API, as validações de entrada
são feitas pelos modelos Pydantic definidos em mainApi.py.
"""


def pedir_texto(mensagem):
    """Pede um texto até que o usuário informe algo que não esteja vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Este campo não pode ficar vazio.")


def pedir_int(mensagem, minimo=1):
    """Pede um número inteiro e garante que seja igual ou maior que o mínimo."""
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= minimo:
                return valor
            print(f"Digite um número maior ou igual a {minimo}.")
        except ValueError:
            print("Digite um número inteiro válido.")


def pedir_float(mensagem, minimo=0):
    """Pede um número decimal; aceita vírgula ou ponto como separador."""
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor >= minimo:
                return valor
            print(f"Digite um valor maior ou igual a {minimo}.")
        except ValueError:
            print("Digite um valor válido.")
