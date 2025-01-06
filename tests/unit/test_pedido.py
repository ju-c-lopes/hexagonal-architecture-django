import pytest
from core.entities.pedido import Pedido
from core.entities.cliente import Cliente
from core.entities.item import Item


def test_pedido_initialization():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    itens = [Item(id=1, nome="Hambúrguer", preco=10.0), Item(id=2, nome="Refrigerante", preco=5.0)]
    pedido = Pedido(id=1, cliente=cliente, itens=itens, status="aberto")

    assert pedido.id == 1
    assert pedido.cliente == cliente
    assert pedido.itens == itens
    assert pedido.status == "aberto"


def test_pedido_calcular_total():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    itens = [Item(id=1, nome="Hambúrguer", preco=10.0), Item(id=2, nome="Refrigerante", preco=5.0)]
    pedido = Pedido(id=1, cliente=cliente, itens=itens, status="aberto")

    total = pedido.calcular_total()

    assert total == 15.0


def test_pedido_sem_itens():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    itens = []
    pedido = Pedido(id=1, cliente=cliente, itens=itens, status="aberto")

    with pytest.raises(ValueError) as exc:
        pedido.calcular_total()

    assert str(exc.value) == "Não é possível criar um pedido sem itens!"
