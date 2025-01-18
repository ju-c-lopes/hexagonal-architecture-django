from unittest.mock import MagicMock, patch

import pytest
from rest_framework.test import APIClient

from core.entities.cliente import Cliente
from core.entities.pedido import Pedido
from core.entities.produto import Categoria, Produto
from core.use_cases.criar_pedido import CriarPedido
from infrastructure.repositories.pedido_repo import PedidoRepository


@pytest.fixture
def mongo_client_mock():
    """Mock para o cliente do MongoDB."""
    return MagicMock()


@pytest.fixture
def cliente_teste():
    """Cliente de teste."""
    return Cliente(
        id='678080fc6d8bebea8dbd25d2',
        nome="João",
        email="joao@email.com",
        cpf="112233445-56",
    )


@pytest.fixture
def clientes_teste():
    """Cliente de teste."""
    return [
        Cliente(
            id=1,
            nome="João",
            email="joao@email.com",
            cpf="112233445-56",
        ),
        Cliente(
            id=2,
            nome="Maria",
            email="maria@email.com",
            cpf="223344556-67",
        ),
    ]


@pytest.fixture
def pedido_repository(mongo_client_mock):
    """Instância do repositório com cliente mockado."""
    db_mock = mongo_client_mock["lanchonete-teste"]
    return PedidoRepository(db_mock)


@pytest.fixture
def pedido_repo_mock():
    """Fixture para criar um mock do repositório de pedidos."""
    return MagicMock()


@pytest.fixture
def produtos_teste():
    """Itens de teste."""
    return [
        {
            "id": 1,
            "nome": "Hambúrguer",
            "descricao": "descrição",
            "categoria": Categoria.LANCHE,
            "preco": 10.0,
        },
        {
            "id": 2,
            "nome": "Refrigerante",
            "descricao": "descrição",
            "categoria": Categoria.BEBIDA,
            "preco": 5.0,
        },
    ]


@pytest.fixture
def cliente_repo_mock(mongo_client_mock):
    """Fixture para criar um mock do repositório de clientes."""
    with patch("adapters.driven.cliente_repo.ClienteRepository") as mock:
        yield mock
        mock.stop()


@pytest.fixture
def criar_pedido_use_case(pedido_repository, cliente_repo_mock):
    """Fixture para o caso de uso CriarPedido."""
    return CriarPedido(pedido_repository, cliente_repo_mock)


@pytest.fixture
def pedido_teste(cliente_teste, produtos_teste):
    """Pedido de teste."""
    return Pedido(
        cliente=cliente_teste,
        produtos=[Produto(**produto) for produto in produtos_teste],
        codigo_do_pedido="123",
        status="PENDENTE",
    )


@pytest.fixture
def pedidos_teste(clientes_teste, produtos_teste):
    """Pedidos de teste."""
    return [
        Pedido(
            cliente=clientes_teste[0],
            produtos=[Produto(**produto) for produto in produtos_teste],
            status="aberto",
        ),
        Pedido(
            cliente=clientes_teste[1],
            produtos=[Produto(**produto) for produto in produtos_teste],
            status="PENDENTE",
        ),
    ]


@pytest.fixture
def api_client():
    """Cliente de testes do DRF."""
    return APIClient()
