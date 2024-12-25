from unittest.mock import MagicMock

import pytest

from core.entities.cliente import Cliente
from core.entities.item import Item
from core.use_cases.criar_pedido import CriarPedido


@pytest.fixture
def pedido_repo_mock():
    """Fixture para criar um mock do repositório de pedidos."""
    return MagicMock()


@pytest.fixture
def cliente_repo_mock():
    """Fixture para criar um mock do repositório de clientes."""
    return MagicMock()


@pytest.fixture
def cliente_teste():
    """Cliente de teste."""
    return Cliente(
        id=1,
        nome="João",
        email="joao@email.com",
        cpf="112233445-56",
    )


@pytest.fixture
def itens_teste():
    """Itens de teste."""
    return [Item(nome="Hambúrguer", preco=10.0), Item(nome="Refrigerante", preco=5.0)]


@pytest.fixture
def criar_pedido_use_case(pedido_repo_mock, cliente_repo_mock):
    """Fixture para o caso de uso CriarPedido."""
    return CriarPedido(pedido_repo_mock, cliente_repo_mock)


def test_criar_pedido_sucesso(
    criar_pedido_use_case, pedido_repo_mock, cliente_teste, itens_teste
):
    # Configuração

    itens = itens_teste
    cliente = cliente_teste

    # Execução
    pedido = criar_pedido_use_case.execute(cliente_data=cliente, itens=itens)

    # Verificações
    pedido_repo_mock.salvar.assert_called_once_with(pedido)
    assert pedido.cliente.__dict__ == cliente.__dict__
    assert len(pedido.itens) == 2
    assert pedido.calcular_total() == 15.0


def test_criar_pedido_sem_itens(criar_pedido_use_case, cliente_teste):
    # Configuração
    itens = []
    cliente = cliente_teste

    # Execução
    with pytest.raises(ValueError) as exc:
        pedido = criar_pedido_use_case.execute(cliente_data=cliente, itens=itens)
        pedido.calcular_total()

    # Verificações
    assert str(exc.value) == "Não é possível criar um pedido sem itens!"
