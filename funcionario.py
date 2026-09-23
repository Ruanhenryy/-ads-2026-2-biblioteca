import pytest

class Funcionario:
    def __init__(self, nome, cpf, cargo):
        self.nome = nome
        self.cargo = cargo
        self.cpf = cpf

    nome_biblioteca = "Biblio do Negroni"

    def bater_ponto(self, cpf, horario):
        print(f"O ponto do funcionario de CPF: {self.cpf} foi registrado no horario: {horario}")

    def cadastrar_livro(self, nome, autor, valor):
        if valor <= 0:
            raise ValueError("O valor não pode ser menor ou igual a 0")
        print(f"Nome: {nome} | autor: {autor} | valor: {valor}")

        

func01 = Funcionario("Pedro", "12312312399", "Repositor")
func02 = Funcionario("Geovanna", "12312312311", "Caixa")

print(f'{func01.cargo}, {func02.cargo}')

func01.bater_ponto("12312312399", "18:20")

func02.cadastrar_livro("Cabeça de um muleke", "Pow's", 100)

print(func01.nome_biblioteca == func02.nome_biblioteca)



