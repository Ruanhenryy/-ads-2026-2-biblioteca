from decimal import Decimal
from comanda import itens_validos, subtotal, desconto, fechar


def test_caminho_normal():
    comanda = ["Emprestimo", "Renovacao", "Multa"]

    resultado = fechar(comanda)

    assert resultado["subtotal"] == Decimal("10.00")
    assert resultado["total"] == Decimal("9.00")


def test_item_fora_do_catalogo():
    comanda = ["Emprestimo", "Livro inexistente"]

    assert itens_validos(comanda) == ["Emprestimo"]
    assert subtotal(comanda) == Decimal("5.00")


def test_regra_desconto_fronteira():
    comanda = ["Emprestimo", "Renovacao", "Multa"]

    assert desconto(comanda, Decimal("10.00")) == Decimal("1.00")


def test_comanda_vazia():
    comanda = []

    assert subtotal(comanda) == Decimal("0.00")
    assert fechar(comanda) == {
        "subtotal": Decimal("0.00"),
        "desconto": Decimal("0.00"),
        "total": Decimal("0.00")
    }


def test_item_invalido_nao_conta_para_desconto():
    comanda = ["Emprestimo", "Renovacao", "Livro inexistente"]

    assert desconto(comanda, Decimal("8.00")) == Decimal("0.00")