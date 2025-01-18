from adapters.driven.database.mongo_connection import get_mongo_client
from infrastructure.serializers import PedidoSerializer, ProdutoSerializer


def test_criar_pedido(api_client, pedido_teste, cliente_teste, produtos_teste):
    produtos_data = [
        ProdutoSerializer(
            produto
        ).data
        for produto in pedido_teste.produtos
    ]
    # s = ProdutoSerializer(pedido_teste.produtos[0].__dict__).data

    pedido = {
        "cliente": cliente_teste.__dict__,
        "produtos": produtos_data,
        "status": pedido_teste.status,
    }

    response = api_client.post("/pedidos/", pedido, format="json")

    assert response.status_code == 201
    assert response.data["cliente"]["nome"] == cliente_teste.nome
    assert len(response.data["produtos"]) == len(produtos_teste)
    assert response.data["status"] == pedido_teste.status

    # Obter o ID do pedido criado
    pedido_cod = response.data["codigo_do_pedido"]

    # Limpar o banco ao final
    get_mongo_client()["lanchonete"]["pedidos"].delete_one({"codigo_do_pedido": pedido_cod})


def test_listar_pedidos(api_client, pedidos_teste):
    pedidos_teste[0] = PedidoSerializer(pedidos_teste[0]).data
    pedidos_teste[1] = PedidoSerializer(pedidos_teste[1]).data

    api_client.post("/pedidos/", pedidos_teste[0], format="json")
    api_client.post("/pedidos/", pedidos_teste[1], format="json")

    response = api_client.get("/pedidos/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data == pedidos_teste

    get_mongo_client()["lanchonete"]["pedidos"].delete_one(
        {"_id": pedidos_teste[0]["id"]}
    )
    get_mongo_client()["lanchonete"]["pedidos"].delete_one(
        {"_id": pedidos_teste[1]["id"]}
    )


def test_buscar_pedido_por_id(api_client, cliente_teste, pedido_teste, produtos_teste):

    produtos_data = [(produto) for produto in produtos_teste]

    pedido = {
        "cliente": cliente_teste.__dict__,
        "produtos": produtos_data,
        "status": pedido_teste.status,
    }

    api_client.post("/pedidos/", pedido, format="json")

    response = api_client.get(f"/pedidos/{pedido['id']}/")

    assert response.status_code == 200
    assert response.data["id"] == pedido_teste.id

    # Obter o ID do pedido criado
    pedido_id = response.data["id"]

    # Limpar o banco ao final
    get_mongo_client()["lanchonete"]["pedidos"].delete_one({"_id": pedido_id})
