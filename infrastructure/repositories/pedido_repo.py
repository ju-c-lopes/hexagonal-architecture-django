from typing import List

from adapters.driven.database.mongo_connection import get_mongo_client
from core.entities.pedido import Pedido
from core.repositories.pedido_repo import PedidoRepository as PedidoRepo
from infrastructure.exceptions import DocumentNotFoundError


class PedidoRepository(PedidoRepo):
    def __init__(self, db=None):
        if db is None:
            client = get_mongo_client()
            db = client["lanchonete"]
        self.collection = db["pedidos"]

    def salvar(self, pedido: Pedido) -> None:
        self.collection.insert_one(
            {
                "cliente": pedido.cliente,
                "produtos": [produto.__dict__ for produto in pedido.produtos],
                "personalizacao": pedido.personalizacao,
                "codigo_do_pedido": pedido.codigo_do_pedido,
                "status": pedido.status,
                "total": pedido.total,
            }
        )
        return pedido

    def buscar_por_codigo_do_pedido(self, codigo_do_pedido: str) -> Pedido:
        pedido_data = self.collection.find_one({"codigo_do_pedido": codigo_do_pedido})
        if pedido_data:
            return pedido_data
        raise DocumentNotFoundError(f"Pedido com id {id} não encontrado.")

    def listar_todos(self) -> List[Pedido]:
        pedidos = self.collection.find()

        return [pedido for pedido in pedidos]
