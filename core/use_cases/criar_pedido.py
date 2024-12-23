from core.entities.pedido import Pedido


class CriarPedido:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, cliente, itens):
        pedido = Pedido(cliente=cliente, itens=itens)
        self.pedido_repository.salvar(pedido)
        return pedido
