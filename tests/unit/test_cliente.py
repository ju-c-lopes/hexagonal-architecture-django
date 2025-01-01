import pytest
from core.entities.cliente import Cliente

def test_cliente_initialization():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    assert cliente.id == 1
    assert cliente.nome == "João"
    assert cliente.email == "joao@email.com"
    assert cliente.cpf == "112233445-56"

def test_cliente_repr():
    cliente = Cliente(id=1, nome="João", email="joao@email.com", cpf="112233445-56")
    assert repr(cliente) == "Cliente(id=1, nome=João, email=joao@email.com, cpf=112233445-56)"
