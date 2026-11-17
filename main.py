"""Versão de terminal do Sistema de Livraria.

O arquivo main.py mantém o menu original. Para executar a versão em API,
utilize mainApi.py com o Uvicorn.
"""

from services.livraria import Livraria


def pedir_texto(mensagem):
    """Solicita um texto e repete a pergunta se o campo ficar vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Este campo não pode ficar vazio.")


def pedir_int(mensagem, minimo=1):
    """Solicita um número inteiro respeitando o valor mínimo."""
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= minimo:
                return valor
            print(f"Digite um número maior ou igual a {minimo}.")
        except ValueError:
            print("Digite um número inteiro válido.")


def pedir_float(mensagem, minimo=0):
    """Solicita um número decimal, aceitando vírgula ou ponto."""
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor >= minimo:
                return valor
            print(f"Digite um valor maior ou igual a {minimo}.")
        except ValueError:
            print("Digite um valor válido.")


def listar_livros(livraria):
    """Exibe os livros cadastrados e a quantidade disponível."""
    livros = livraria.listar_livros()
    if not livros:
        print("Nenhum livro cadastrado.")
        return 
    print("\n--- ESTOQUE DE LIVROS ---")
    for livro in livros:
        print(
            f"ID: {livro['id']} | ISBN: {livro['isbn']} | "
            f"{livro['titulo']} — {livro['autor']} | "
            f"R$ {livro['preco']:.2f} | Estoque: {livro['estoque']}"
        )


def cadastrar_cliente(livraria):
    """Lê os dados do cliente e chama a regra de cadastro."""
    print("\n--- CADASTRAR CLIENTE ---")
    try:
        cliente_id = livraria.cadastrar_cliente(
            pedir_texto("Nome: "),
            pedir_texto("CPF: "),
            input("Telefone: ").strip(),
            input("E-mail: ").strip()
        )
        print(f"Cliente cadastrado com sucesso! ID: {cliente_id}")
    except ValueError as erro:
        print(f"Não foi possível cadastrar: {erro}")


def cadastrar_funcionario(livraria):
    """Lê os dados do funcionário e chama a regra de cadastro."""
    print("\n--- CADASTRAR FUNCIONÁRIO ---")
    try:
        funcionario_id = livraria.cadastrar_funcionario(
            pedir_texto("Nome: "),
            pedir_texto("CPF: "),
            input("Telefone: ").strip(),
            input("E-mail: ").strip(),
            pedir_texto("Matrícula: "),
            pedir_texto("Cargo: ")
        )
        print(f"Funcionário cadastrado com sucesso! ID: {funcionario_id}")
    except ValueError as erro:
        print(f"Não foi possível cadastrar: {erro}")


def cadastrar_livro(livraria):
    """Lê os dados do livro e chama a regra de cadastro."""
    print("\n--- CADASTRAR LIVRO ---")
    try:
        livro_id = livraria.cadastrar_livro(
            pedir_texto("ISBN/código único: "),
            pedir_texto("Título: "),
            pedir_texto("Autor: "),
            pedir_float("Preço (R$): "),
            pedir_int("Quantidade inicial em estoque: ", minimo=0)
        )
        print(f"Livro cadastrado com sucesso! ID: {livro_id}")
    except ValueError as erro:
        print(f"Não foi possível cadastrar: {erro}")


def registrar_compra(livraria):
    """Coleta cliente, funcionário e itens para formar uma compra."""
    print("\n--- REGISTRAR COMPRA ---")
    clientes = livraria.listar_clientes()
    funcionarios = livraria.listar_funcionarios()
    livros = livraria.listar_livros()

    if not clientes:
        print("Cadastre pelo menos um cliente antes de registrar uma compra.")
        return
    if not funcionarios:
        print("Cadastre pelo menos um funcionário antes de registrar uma compra.")
        return
    if not livros:
        print("Cadastre pelo menos um livro antes de registrar uma compra.")
        return

    print("\nClientes:")
    for c in clientes:
        print(f"ID: {c['id']} | {c['nome']} | CPF: {c['cpf']}")
    cliente_id = pedir_int("ID do cliente: ")

    print("\nFuncionários:")
    for f in funcionarios:
        print(f"ID: {f['id']} | {f['nome']} | Matrícula: {f['matricula']}")
    funcionario_id = pedir_int("ID do funcionário: ")

    itens = []
    while True:
        listar_livros(livraria)
        livro_id = pedir_int("ID do livro (0 para concluir): ", minimo=0)
        if livro_id == 0:
            break
        quantidade = pedir_int("Quantidade: ")
        itens.append((livro_id, quantidade))
        if input("Adicionar outro livro? (s/n): ").strip().lower() != "s":
            break

    if not itens:
        print("Compra cancelada: nenhum item selecionado.")
        return

    try:
        compra_id, total = livraria.registrar_compra(cliente_id, funcionario_id, itens)
        print(f"\nCompra #{compra_id} registrada! Total: R$ {total:.2f}")
    except (ValueError, RuntimeError) as erro:
        print(f"Não foi possível registrar a compra: {erro}")


def historico_cliente(livraria):
    """Mostra as compras já registradas para um cliente."""
    print("\n--- HISTÓRICO DE COMPRAS ---")
    clientes = livraria.listar_clientes()
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for cliente in clientes:
        print(f"ID: {cliente['id']} | {cliente['nome']} | CPF: {cliente['cpf']}")
    cliente_id = pedir_int("ID do cliente: ")
    compras = livraria.historico_cliente(cliente_id)
    if not compras:
        print("Nenhuma compra encontrada para este cliente.")
        return
    for compra in compras:
        print(
            f"\nCompra #{compra['id']} | Data: {compra['data']} | "
            f"Funcionário: {compra['funcionario']} | Total: R$ {compra['total']:.2f}"
        )
        for item in compra["itens"]:
            print(
                f"  - {item['titulo']} | Quantidade: {item['quantidade']} | "
                f"Preço unitário: R$ {item['preco_unitario']:.2f} | "
                f"Subtotal: R$ {item['subtotal']:.2f}"
            )


def pesquisar_livro(livraria):
    """Pesquisa livros por título, autor ou ISBN."""
    termo = pedir_texto("Digite título, autor ou ISBN: ")
    resultados = livraria.buscar_livros(termo)
    if not resultados:
        print("Nenhum livro encontrado.")
        return
    for livro in resultados:
        print(
            f"ID: {livro['id']} | {livro['titulo']} — {livro['autor']} | "
            f"R$ {livro['preco']:.2f} | Estoque: {livro['estoque']}"
        )


def menu():
    """Cria a conexão e apresenta o menu principal do sistema."""
    livraria = Livraria()
    # Cada opção associa um número, uma descrição e a função que será chamada.
    # O uso de lambda permite executar a função somente quando a opção é escolhida.
    opcoes = {
        "1": ("Cadastrar cliente", lambda: cadastrar_cliente(livraria)),
        "2": ("Cadastrar funcionário", lambda: cadastrar_funcionario(livraria)),
        "3": ("Cadastrar livro", lambda: cadastrar_livro(livraria)),
        "4": ("Consultar estoque", lambda: listar_livros(livraria)),
        "5": ("Pesquisar livro", lambda: pesquisar_livro(livraria)),
        "6": ("Registrar compra", lambda: registrar_compra(livraria)),
        "7": ("Histórico de compras de cliente", lambda: historico_cliente(livraria)),
        "8": ("Listar clientes", lambda: print("\n".join(
            f"ID: {c['id']} | {c['nome']} | CPF: {c['cpf']}"
            for c in livraria.listar_clientes()
        ) or "Nenhum cliente cadastrado.")),
        "9": ("Listar funcionários", lambda: print("\n".join(
            f"ID: {f['id']} | {f['nome']} | Matrícula: {f['matricula']} | Cargo: {f['cargo']}"
            for f in livraria.listar_funcionarios()
        ) or "Nenhum funcionário cadastrado.")),
    }

    # O finally garante que o banco seja fechado mesmo se o menu for encerrado
    # ou se ocorrer algum erro durante a execução.
    try:
        while True:
            print("\n" + "=" * 42)
            print("       SISTEMA DE LIVRARIA")
            print("=" * 42)
            for numero, (descricao, _) in opcoes.items():
                print(f"{numero}. {descricao}")
            print("0. Sair")
            escolha = input("\nEscolha uma opção: ").strip()

            if escolha == "0":
                print("Sistema encerrado. Até mais!")
                break
            acao = opcoes.get(escolha)
            if acao:
                acao[1]()
            else:
                print("Opção inválida.")
    finally:
        livraria.fechar()


if __name__ == "__main__":
    menu()
