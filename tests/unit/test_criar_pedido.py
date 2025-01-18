import pytest

from core.entities.produto import Produto
from core.use_cases.criar_pedido import CriarPedido


def test_criar_pedido_sucesso(
    cliente_repo_mock,
    pedido_repo_mock,
    pedido_teste,
    cliente_teste,
    produtos_teste,
):
    # Configuração
    produtos = [
        Produto(**produto)
        for produto in produtos_teste
    ]
    pedido_repo_mock.salvar.return_value = pedido_teste
    cliente_repo_mock.buscar_por_cpf.return_value = cliente_teste
    criar_pedido = CriarPedido(pedido_repo_mock, cliente_repo_mock)

    # Execução
    pedido = criar_pedido.execute(cliente_data=cliente_teste.__dict__, produtos=produtos)
    # breakpoint()
    # Verificações
    pedido_repo_mock.salvar.assert_called_once_with(pedido)
    assert pedido.cliente == cliente_teste
    assert len(pedido.produtos) == 2
    assert pedido.calcular_total() == 15.0


def test_criar_pedido_sem_produtos(pedido_teste):
    # Configuração
    pedido_teste.produtos = []

    # Execução
    with pytest.raises(ValueError) as exc:
        pedido_teste.calcular_total()

    # Verificações
    assert str(exc.value) == "Não é possível criar um pedido sem produtos!"
