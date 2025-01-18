from unittest.mock import MagicMock

from core.entities.cliente import Cliente
from core.entities.pedido import Pedido
from core.entities.produto import Categoria, Produto
from infrastructure.repositories.pedido_repo import PedidoRepository


def test_salvar_pedido(
    pedido_repository: PedidoRepository,
    mongo_client_mock: MagicMock,
    cliente_teste: Cliente,
):
    produtos = [
        Produto(
            id=1,
            nome="Hambúrguer",
            descricao="descrição",
            categoria=Categoria.LANCHE,
            preco=10.0,
            disponivel=True,
        )
    ]
    pedido = Pedido(
        cliente=cliente_teste,
        produtos=produtos,
        personalizacao="personalizacao",
        codigo_do_pedido="20250101-010",
        status="aberto",
    )
    pedido.total = pedido.calcular_total()

    pedido_repository.salvar(pedido)

    # Verifica se o método insert_one foi chamado com os dados corretos
    mongo_client_mock["lanchonete-teste"]["pedidos"].insert_one.assert_called_once_with(
        {
            "cliente": cliente_teste,
            "produtos": [
                {
                    "_id": 1,
                    "nome": "Hambúrguer",
                    "descricao": "descrição",
                    "categoria": Categoria.LANCHE,
                    "preco": 10.0,
                    "disponivel": True,
                }
            ],
            "personalizacao": pedido.personalizacao,
            "codigo_do_pedido": pedido.codigo_do_pedido,
            "status": "aberto",
            "total": pedido.total,
        }
    )


def test_buscar_por_codigo_do_pedido(
    pedido_repository: PedidoRepository,
    mongo_client_mock: MagicMock,
    cliente_teste: Cliente,
):
    # Mock do retorno do find_one
    mongo_client_mock["lanchonete"]["pedidos"].find_one.return_value = {
        "_id": "123",
        "cliente": cliente_teste.__dict__,
        "produtos": [
            {
                "id": 1,
                "nome": "Hambúrguer",
                "descricao": "descrição",
                "categoria": Categoria.LANCHE,
                "preco": 10.0,
            }
        ],
        "personalizacao": "personalizacao",
        "codigo_do_pedido": "123",
        "status": "aberto",
        "total": 10.0,
    }

    pedido = pedido_repository.buscar_por_codigo_do_pedido("123")

    assert pedido["cliente"]["nome"] == "João"
    assert len(pedido["produtos"]) == 1
    assert pedido["produtos"][0]["id"] == 1
    assert pedido["produtos"][0]["nome"] == "Hambúrguer"
    assert pedido["produtos"][0]["categoria"] == Categoria.LANCHE
    assert pedido["produtos"][0]["preco"] == 10.0
    assert pedido["personalizacao"] == "personalizacao"
    assert pedido["codigo_do_pedido"] == "123"
    assert pedido["status"] == "aberto"
    assert pedido["total"] == 10.0


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
            "produtos": [
                {
                    "id": 1,
                    "nome": "Hambúrguer",
                    "descricao": "descrição",
                    "categoria": Categoria.LANCHE,
                    "preco": 10.0,
                }
            ],
            "status": "aberto",
        }
    ]

    pedidos = pedido_repository.listar_todos()

    assert len(pedidos) == 1
    assert pedidos[0]["cliente"]["nome"] == "João"
    assert len(pedidos[0]["produtos"]) == 1
    assert pedidos[0]["produtos"][0]["nome"] == "Hambúrguer"
    assert pedidos[0]["produtos"][0]["categoria"] == Categoria.LANCHE
    assert pedidos[0]["produtos"][0]["preco"] == 10.0
