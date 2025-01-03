from typing import List

from core.entities.item import Item
from core.entities.pedido import Pedido
from core.repositories.pedido_repo import PedidoRepository
from infrastructure.database.mongo_connection import get_mongo_client


class MongoPedidoRepository(PedidoRepository):
    def __init__(self, db=None):
        if db is None:
            client = get_mongo_client()
            db = client["lanchonete"]
        self.collection = db["pedidos"]

    def salvar(self, pedido: Pedido) -> None:
        self.collection.insert_one(
            {
                "_id": pedido.id,
                "cliente": pedido.cliente.__dict__,
                "itens": [item.__dict__ for item in pedido.itens],
                "status": pedido.status,
            }
        )

    def buscar_por_id(self, id: str) -> Pedido:
        pedido_data = self.collection.find_one({"_id": id})
        if pedido_data:
            return Pedido(
                id=id,
                cliente=pedido_data["cliente"],
                itens=[Item(id=item["id"], nome=item["nome"], preco=item["preco"]) for item in pedido_data["itens"]],
                status=pedido_data["status"],
            )
        return None

    def listar_todos(self) -> List[Pedido]:
        pedidos = self.collection.find()
        return [
            Pedido(
                id=pedido["_id"],
                cliente=pedido["cliente"],
                itens=[Item(id=item["id"], nome=item["nome"], preco=item["preco"]) for item in pedido["itens"]],
                status=pedido["status"],
            )
            for pedido in pedidos
        ]
