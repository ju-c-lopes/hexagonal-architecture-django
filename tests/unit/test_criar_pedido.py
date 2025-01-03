import pytest


def test_criar_pedido_sucesso(
    criar_pedido_use_case, pedido_repo_mock, cliente_teste, itens_teste
):
    # Configuração

    itens = itens_teste
    cliente = cliente_teste

    # Execução
    pedido = criar_pedido_use_case.execute(cliente_data=cliente, itens=itens)

    # Verificações
    pedido_repo_mock.salvar.assert_called_once_with(pedido)
    assert pedido.cliente.__dict__ == cliente.__dict__
    assert len(pedido.itens) == 2
    assert pedido.calcular_total() == 15.0
    assert pedido.itens[0].id is not None
    assert pedido.itens[1].id is not None


def test_criar_pedido_sem_itens(criar_pedido_use_case, cliente_teste):
    # Configuração
    itens = []
    cliente = cliente_teste

    # Execução
    with pytest.raises(ValueError) as exc:
        pedido = criar_pedido_use_case.execute(cliente_data=cliente, itens=itens)
        pedido.calcular_total()

    # Verificações
    assert str(exc.value) == "Não é possível criar um pedido sem itens!"
