from core.entities.pedido import Pedido
from core.repositories.pedido_repo import PedidoRepository


class ListarPedido:
    def __init__(self, pedido_repository: PedidoRepository):
        self.pedido_repository = pedido_repository

    def execute(self, codigo_do_pedido: str) -> Pedido:
        # Recupera o pedido por id
        pedido = self.pedido_repository.buscar_por_codigo_do_pedido(codigo_do_pedido)
        return pedido
