class Pessoa:
    """Classe-base com os dados comuns de uma pessoa."""

    def __init__(self, nome, cpf, telefone="", email=""):
        self.nome = nome.strip()
        self.cpf = cpf.strip()
        self.telefone = telefone.strip()
        self.email = email.strip()

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"
