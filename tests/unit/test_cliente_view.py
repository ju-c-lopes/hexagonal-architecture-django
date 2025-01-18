from unittest.mock import Mock

import pytest
from rest_framework.test import APIRequestFactory

from adapters.driver.cliente_view import ClienteAPIView, ClienteDetalheAPIView
from core.entities.cliente import Cliente


def cliente_mock():
    return {
        "_id": "67893703141703acbb0edd53",
        "nome": "João",
        "email": "joao@email.com",
        "cpf": "112233445-56",
    }


@pytest.fixture
def cliente_repo_mock():
    return Mock()


@pytest.fixture
def cliente_teste():
    return Cliente(
        nome="João",
        email="joao@email.com",
        cpf="112233445-56",
    )


def test_criar_cliente(cliente_repo_mock, cliente_teste):
    # Configuração
    cliente_data = {
        "nome": cliente_teste.nome,
        "email": cliente_teste.email,
        "cpf": cliente_teste.cpf,
    }

    # Execução
    factory = APIRequestFactory()
    request = factory.post("/clientes/", cliente_data, format="json")
    view = ClienteAPIView(cliente_repo=cliente_repo_mock)

    drf_request = view.initialize_request(request)
    response = view.post(drf_request)

    # Verificação
    assert response.status_code == 201
    assert response.data["nome"] == cliente_teste.nome
    assert response.data["email"] == cliente_teste.email
    assert response.data["cpf"] == cliente_teste.cpf


def test_listar_clientes(cliente_repo_mock):
    # Arrange
    cliente_data = cliente_mock()
    cliente_repo_mock.listar.return_value = [cliente_data]
    factory = APIRequestFactory()
    request = factory.get("/clientes/")
    view = ClienteAPIView(cliente_repo=cliente_repo_mock)

    # Act
    drf_request = view.initialize_request(request)
    response = view.get(drf_request)

    # Assert
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert cliente_data in response.data


def test_buscar_cliente_por_cpf(cliente_repo_mock):
    # Arrange
    cliente_data = cliente_mock()
    cpf = cliente_data["cpf"]
    cliente_repo_mock.executar.return_value = (
        cliente_data  # Mock use case to return a single client by CPF
    )

    factory = APIRequestFactory()
    request = factory.get(f"/clientes/{cpf}/")
    view = ClienteDetalheAPIView(listar_cliente_use_case=cliente_repo_mock)

    # Act
    drf_request = view.initialize_request(request)
    response = view.get(drf_request, cpf=cpf)

    # Assert
    assert response.status_code == 200
    assert response.data == cliente_data


def test_buscar_cliente_por_cpf_nao_encontrado(cliente_repo_mock):
    # Arrange
    cpf = "112233445-56"
    cliente_repo_mock.executar.side_effect = Exception("Cliente não encontrado")

    factory = APIRequestFactory()
    request = factory.get(f"/clientes/{cpf}/")
    view = ClienteDetalheAPIView(listar_cliente_use_case=cliente_repo_mock)

    # Act
    drf_request = view.initialize_request(request)
    response = view.get(drf_request, cpf=cpf)

    # Assert
    assert response.status_code == 404
    assert response.data["error"] == "Cliente não encontrado"
