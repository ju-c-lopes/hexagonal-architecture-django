from rest_framework.test import APIRequestFactory

from infrastructure.views.cliente_view import ClienteAPIView


def test_criar_cliente(cliente_repo_mock, cliente_teste):
    # Configuração
    cliente_data = {
        "id": cliente_teste.id,
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
    assert response.data == {"id": 1, "nome": "João", "email": "joao@email.com", "cpf": "112233445-56"}


def test_listar_clientes(cliente_repo_mock):
    # Configuração
    cliente_repo_mock.listar_todos.return_value = [
        {"id": 1, "nome": "João", "email": "joao@email.com", "cpf": "112233445-56"},
        {"id": 2, "nome": "Maria", "email": "maria@email.com", "cpf": "223344556-67"},
    ]

    factory = APIRequestFactory()
    request = factory.get("/clientes/")
    view = ClienteAPIView(cliente_repo=cliente_repo_mock)

    response = view.get(request)

    # Verificação
    assert response.status_code == 200
    assert response.data == [
        {"id": 1, "nome": "João", "email": "joao@email.com", "cpf": "112233445-56"},
        {"id": 2, "nome": "Maria", "email": "maria@email.com", "cpf": "223344556-67"},
    ]


def test_buscar_cliente_por_id(cliente_repo_mock):
    # Configuração
    cliente_repo_mock.buscar_por_id.return_value = {
        "id": 1,
        "nome": "João",
        "email": "joao@email.com",
        "cpf": "112233445-56",
    }

    factory = APIRequestFactory()
    request = factory.get("/clientes/1/")
    view = ClienteAPIView(cliente_repo=cliente_repo_mock)

    # Execução
    response = view.get(request, id=1)

    # Verificação
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "nome": "João",
        "email": "joao@email.com",
        "cpf": "112233445-56",
    }
