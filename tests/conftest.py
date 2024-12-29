from unittest.mock import MagicMock, patch

import pytest
from rest_framework.test import APIClient

from core.entities.cliente import Cliente
from core.entities.item import Item
from core.use_cases.criar_pedido import CriarPedido
from infrastructure.repositories.pedido_repo import MongoPedidoRepository


@pytest.fixture
def mongo_client_mock():
    """Mock para o cliente do MongoDB."""
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
def clientes_teste():
    """Cliente de teste."""
    return [Cliente(
        id=1,
        nome="João",
        email="joao@email.com",
        cpf="112233445-56",
    ), Cliente(
        id=2,
        nome="Maria",
        email="maria@email.com",
        cpf="223344556-67",
    )]


@pytest.fixture
def pedido_repository(mongo_client_mock):
    """Instância do repositório com cliente mockado."""
    db_mock = mongo_client_mock["lanchonete-teste"]
    return MongoPedidoRepository(db_mock)


@pytest.fixture
def pedido_repo_mock():
    """Fixture para criar um mock do repositório de pedidos."""
    return MagicMock()


@pytest.fixture
def itens_teste():
    """Itens de teste."""
    return [Item(nome="Hambúrguer", preco=10.0), Item(nome="Refrigerante", preco=5.0)]


@pytest.fixture
def cliente_repo_mock(mongo_client_mock):
    """Fixture para criar um mock do repositório de clientes."""
    with patch('infrastructure.repositories.cliente_repo.ClienteRepository') as mock:
        yield mock
        mock.stop()


@pytest.fixture
def criar_pedido_use_case(pedido_repo_mock, cliente_repo_mock):
    """Fixture para o caso de uso CriarPedido."""
    return CriarPedido(pedido_repo_mock, cliente_repo_mock)


@pytest.fixture
def api_client():
    """Cliente de testes do DRF."""
    return APIClient()
