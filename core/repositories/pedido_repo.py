from abc import ABC, abstractmethod
from typing import List

from core.entities.pedido import Pedido


class PedidoRepository(ABC):
    """Interface de contrato para repositórios de pedidos."""

    @abstractmethod
    def salvar(self, pedido: Pedido) -> None:
        """Salva um pedido no repositório."""
        pass

    @abstractmethod
    def buscar_por_id(self, id: str) -> Pedido:
        """Busca um pedido pelo ID."""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Pedido]:
        """Retorna uma lista de todos os pedidos."""
        pass
