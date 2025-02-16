from unittest.mock import MagicMock

from core.entities.cliente import Cliente
from core.entities.item import Item
from core.entities.pedido import Pedido
from infrastructure.repositories.pedido_repo import PedidoRepository


def test_salvar_pedido(
    pedido_repository: PedidoRepository,
    mongo_client_mock: MagicMock,
    cliente_teste: Cliente,
):
    itens = [Item(id=1, nome="Hambúrguer", preco=10.0)]
    pedido = Pedido(id="123", cliente=cliente_teste, itens=itens, status="aberto")

    pedido_repository.salvar(pedido)

    # Verifica se o método insert_one foi chamado com os dados corretos
    mongo_client_mock["lanchonete-teste"]["pedidos"].insert_one.assert_called_once_with(
        {
            "_id": "123",
            "cliente": cliente_teste.__dict__,
            "itens": [{"id": 1, "nome": "Hambúrguer", "preco": 10.0}],
            "status": "aberto",
        }
    )


def test_buscar_por_id(
    pedido_repository: PedidoRepository,
    mongo_client_mock: MagicMock,
    cliente_teste: Cliente,
):
    # Mock do retorno do find_one
    mongo_client_mock["lanchonete"]["pedidos"].find_one.return_value = {
        "_id": "123",
        "cliente": {
            "id": cliente_teste.id,
            "nome": cliente_teste.nome,
            "email": cliente_teste.email,
            "cpf": cliente_teste.cpf,
        },
        "itens": [{"id": 1, "nome": "Hambúrguer", "preco": 10.0}],
        "status": "aberto",
    }

    pedido = pedido_repository.buscar_por_id("123")

    assert pedido.cliente.nome == "João"
    assert len(pedido.itens) == 1
    assert pedido.itens[0].id == 1
    assert pedido.itens[0].nome == "Hambúrguer"
    assert pedido.itens[0].preco == 10.0


def test_listar_todos(
    pedido_repository: PedidoRepository,
    mongo_client_mock: MagicMock,
    cliente_teste: Cliente,
):
    # Mock do retorno do find
    mongo_client_mock["lanchonete"]["pedidos"].find.return_value = [
        {
            "_id": "123",
            "cliente": cliente_teste.__dict__,
            "itens": [{"id": 1, "nome": "Hambúrguer", "preco": 10.0}],
            "status": "aberto",
        }
    ]

    pedidos = pedido_repository.listar_todos()

    assert len(pedidos) == 1
    assert pedidos[0].cliente.nome == "João"
    assert len(pedidos[0].itens) == 1
    assert pedidos[0].itens[0].id == 1
    assert pedidos[0].itens[0].nome == "Hambúrguer"
    assert pedidos[0].itens[0].preco == 10.0
