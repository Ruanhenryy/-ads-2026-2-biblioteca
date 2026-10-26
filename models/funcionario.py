from models.pessoa import Pessoa


class Funcionario(Pessoa):
    """Representa um funcionário da livraria."""

    def __init__(self, nome, cpf, telefone, email, matricula, cargo):
        super().__init__(nome, cpf, telefone, email)
        self.matricula = matricula.strip()
        self.cargo = cargo.strip()
