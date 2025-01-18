import pytest

from core.entities import TipoCadastro
from core.entities.cliente import Cliente
from core.entities.pedido import Pedido
from core.entities.produto import Categoria, Produto


def test_pedido_iniciar_com_dados_validos():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    produtos = [
        Produto(id=1, nome="Hambúrguer", descricao="Descrição do produto", categoria=Categoria.LANCHE, preco=10.0),
        Produto(
            id=2, nome="Refrigerante", descricao="Descrição 2 do produto", categoria=Categoria.BEBIDA, preco=5.0
        ),
    ]
    pedido = Pedido(
        cliente=cliente,
        cadastro=None,
        produtos=produtos,
        codigo_do_pedido="123ABC",
        status="aberto",
    )
    pedido.cadastro = pedido.set_cadastro()

    assert pedido.cliente == cliente
    assert pedido.produtos == produtos
    assert pedido.codigo_do_pedido == "123ABC"
    assert pedido.status == "aberto"
    assert pedido.total == 15.0
    assert pedido.cadastro == TipoCadastro[1][0]


def test_pedido_calcular_total():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    produtos = [
        Produto(id=1, nome="Hambúrguer", descricao="descricao", categoria=Categoria.LANCHE, preco=10.0),
        Produto(id=2, nome="Refrigerante", descricao="descricao", categoria=Categoria.BEBIDA, preco=5.0),
    ]
    pedido = Pedido(cliente=cliente, produtos=produtos, status="aberto")

    total = pedido.calcular_total()

    assert total == 15.0


def test_pedido_sem_produtos():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    produtos = []

    with pytest.raises(ValueError) as exc:
        Pedido(cliente=cliente, produtos=produtos, status="aberto")

    assert str(exc.value) == "Não é possível criar um pedido sem produtos!"


def test_pedido_sem_codigo_do_pedido():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    produtos = [
        Produto(id=1, nome="Hambúrguer", descricao="Descrição", categoria=Categoria.LANCHE, preco=10.0),
        Produto(id=2, nome="Refrigerante", descricao="Descrição", categoria=Categoria.BEBIDA, preco=5.0),
    ]
    pedido = Pedido(cliente=cliente, produtos=produtos)

    assert pedido.codigo_do_pedido is None
