class Pessoa:
    """Classe-base com os dados que clientes e funcionários têm em comum.

    A ideia da herança é evitar repetir os mesmos atributos e o mesmo
    comportamento nas classes Cliente e Funcionario.
    """

    def __init__(self, nome, cpf, telefone="", email=""):
        # strip() remove espaços que possam ter sido digitados no início/fim.
        self.nome = nome.strip()
        self.cpf = cpf.strip()
        self.telefone = telefone.strip()
        self.email = email.strip()

    def __str__(self):
        """Retorna uma representação simples da pessoa em texto."""
        return f"{self.nome} (CPF: {self.cpf})"
