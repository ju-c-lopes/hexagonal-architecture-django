import pytest
from rest_framework.test import APIClient
from core.entities.cliente import Cliente
from core.entities.item import Item
from core.entities.pedido import Pedido
from infrastructure.repositories.cliente_repo import ClienteRepository
from infrastructure.repositories.pedido_repo import MongoPedidoRepository


def test_criar_pedido(api_client, cliente_teste, itens_teste):
    cliente_data = {
        "id": cliente_teste.id,
        "nome": cliente_teste.nome,
        "email": cliente_teste.email,
        "cpf": cliente_teste.cpf,
    }
    itens_data = [{"nome": item.nome, "preco": item.preco} for item in itens_teste]

    response = api_client.post("/pedidos/", {"cliente": cliente_data, "itens": itens_data}, format="json")

    assert response.status_code == 201
    assert response.data["cliente"]["nome"] == cliente_teste.nome
    assert len(response.data["itens"]) == len(itens_teste)

def test_listar_pedidos(api_client, pedido_repo, pedido_teste):
    pedido_repo.salvar(pedido_teste)

    response = api_client.get("/pedidos/")

    assert response.status_code == 200
    assert len(response.data) > 0

def test_buscar_pedido_por_id(api_client, pedido_repo, pedido_teste):
    pedido_repo.salvar(pedido_teste)

    response = api_client.get(f"/pedidos/{pedido_teste.id}/")

    assert response.status_code == 200
    assert response.data["id"] == pedido_teste.id
