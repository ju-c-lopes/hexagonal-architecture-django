from unittest.mock import MagicMock

import pytest

from core.entities.pedido import Item, Pedido  # noqa
from core.use_cases.criar_pedido import CriarPedido


@pytest.fixture
def pedido_repo_mock():
    """Fixture para criar um mock do repositório de pedidos."""
    return MagicMock()


@pytest.fixture
def criar_pedido_use_case(pedido_repo_mock):
    """Fixture para o caso de uso CriarPedido."""
    return CriarPedido(pedido_repo_mock)


def test_criar_pedido_sucesso(criar_pedido_use_case, pedido_repo_mock):
    # Configuração
    itens = [Item(nome="Hambúrguer", preco=10.0), Item(nome="Refrigerante", preco=5.0)]
    cliente = "Cliente Teste"

    # Execução
    pedido = criar_pedido_use_case.execute(cliente=cliente, itens=itens)

    # Verificações
    pedido_repo_mock.salvar.assert_called_once_with(pedido)
    assert pedido.cliente == cliente
    assert len(pedido.itens) == 2
    assert pedido.calcular_total() == 15.0


def test_criar_pedido_sem_itens(criar_pedido_use_case):
    # Configuração
    itens = []
    cliente = "Cliente Teste"

    # Execução
    with pytest.raises(ValueError) as exc:
        pedido = criar_pedido_use_case.execute(cliente=cliente, itens=itens)
        pedido.calcular_total()

    # Verificações
    assert str(exc.value) == "Não é possível criar um pedido sem itens!"
