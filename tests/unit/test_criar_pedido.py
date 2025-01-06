import pytest

from core.use_cases.criar_pedido import CriarPedido
from infrastructure.serializers import ItemSerializer


def test_criar_pedido_sucesso(
    cliente_repo_mock, pedido_repo_mock, cliente_teste, itens_teste
):
    # Configuração
    itens = ItemSerializer(itens_teste, many=True).data
    cliente_repo_mock.buscar_por_id.return_value = cliente_teste
    criar_pedido = CriarPedido(pedido_repo_mock, cliente_repo_mock)

    # Execução
    pedido = criar_pedido.execute(cliente_data=cliente_teste, itens=itens)

    # Verificações
    pedido_repo_mock.salvar.assert_called_once_with(pedido)
    assert pedido.cliente.__dict__ == cliente_teste.__dict__
    assert len(pedido.itens) == 2
    assert pedido.calcular_total() == 15.0
    assert pedido.itens[0].id is not None
    assert pedido.itens[1].id is not None


def test_criar_pedido_sem_itens(pedido_teste):
    # Configuração
    pedido_teste.itens = []

    # Execução
    with pytest.raises(ValueError) as exc:
        pedido_teste.calcular_total()

    # Verificações
    assert str(exc.value) == "Não é possível criar um pedido sem itens!"
