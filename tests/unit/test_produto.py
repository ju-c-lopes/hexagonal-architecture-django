import pytest

from core.entities.produto import Categoria, Produto


def test_produto_initialization():
    produto = Produto(
        id=1,
        nome="Hambúrguer",
        categoria=Categoria.LANCHE,
        descricao="descrição",
        preco=10.0,
    )

    assert produto._id == 1
    assert produto.nome == "Hambúrguer"
    assert produto.descricao == "descrição"
    assert produto.preco == 10.0
    assert produto.disponivel is True


def test_produto_repr():
    produto = Produto(
        id=1,
        nome="Hambúrguer",
        descricao="Delicioso hambúrguer artesanal",
        categoria=Categoria.LANCHE,
        preco=10.0,
    )
    expected_repr = """
Categoria.LANCHE:
    Hambúrguer
    Preço = R$ 10.00
"""
    assert repr(produto) == expected_repr


def test_produto_repr_com_valores_diferentes():
    produto = Produto(
        id=2,
        nome="Refrigerante",
        descricao="Refrigerante gelado",
        categoria=Categoria.BEBIDA,
        preco=5.0,
    )
    expected_repr = """
Categoria.BEBIDA:
    Refrigerante
    Preço = R$ 5.00
"""
    assert repr(produto) == expected_repr


def test_produto_com_preco_invalido():
    with pytest.raises(ValueError) as exc:
        Produto(
            id=1,
            nome="Hambúrguer",
            descricao="Delicioso hambúrguer artesanal",
            categoria=Categoria.LANCHE,
            preco=-10.0,
        )

    assert str(exc.value) == "Preço do produto não pode ser negativo!"


def test_produto_indisponivel():
    produto = Produto(
        id=1,
        nome="Hambúrguer",
        descricao="Delicioso hambúrguer artesanal",
        categoria=Categoria.LANCHE,
        preco=10.0,
        disponivel=False,
    )

    assert produto.disponivel is False
