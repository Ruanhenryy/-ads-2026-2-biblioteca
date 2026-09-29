from comanda import Comanda


def test_itens_validos():
    comanda = Comanda([
        "Emprestimo",
        "Renovacao",
        "Livro inexistente"
    ])

    assert comanda.itens_validos() == [
        "Emprestimo",
        "Renovacao"
    ]


def test_subtotal():
    comanda = Comanda([
        "Emprestimo",
        "Renovacao",
        "Emprestimo"
    ])

    assert comanda.subtotal() == 13.00


def test_itens_invalidos():
    comanda = Comanda([
        "Emprestimo",
        "Livro inexistente"
    ])

    assert comanda.itens_validos() == ["Emprestimo"]


def test_comanda_vazia():
    comanda = Comanda([])

    assert comanda.itens_validos() == []
    assert comanda.subtotal() == 0.00


def test_itens_deve_ser_lista():
    try:
        Comanda("Emprestimo")
        assert False
    except ValueError:
        assert True