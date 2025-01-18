from typing import List

from core.entities.pedido import Pedido
from core.repositories.pedido_repo import PedidoRepository


class ListarPedidos:
    def __init__(self, pedido_repository: PedidoRepository):
        self.pedido_repository = pedido_repository

    def execute(self) -> List[Pedido]:
        # Recupera os pedidos do repositório
        pedidos = self.pedido_repository.listar_todos()

        return pedidos
