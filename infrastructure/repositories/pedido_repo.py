from typing import List

from core.entities.cliente import Cliente
from core.entities.item import Item
from core.entities.pedido import Pedido
from core.repositories.pedido_repo import PedidoRepository as PedidoRepo
from infrastructure.database.mongo_connection import get_mongo_client
from infrastructure.exceptions import DocumentNotFoundError


class PedidoRepository(PedidoRepo):
    def __init__(self, db=None):
        if db is None:
            client = get_mongo_client()
            db = client["lanchonete"]
        self.collection = db["pedidos"]

    def salvar(self, pedido: Pedido) -> None:
        result = self.collection.insert_one(
            {
                "_id": None if pedido.id is None else pedido.id,
                "cliente": pedido.cliente.__dict__,
                "itens": [item.__dict__ for item in pedido.itens],
                "status": pedido.status,
            }
        )
        pedido.id = str(result.inserted_id) if pedido.id is None else pedido.id

        return None

    def buscar_por_id(self, id: str) -> Pedido:
        pedido_data = self.collection.find_one({"_id": id})
        if pedido_data:
            return Pedido(
                id=id,
                cliente=Cliente(
                    pedido_data["cliente"]["id"],
                    pedido_data["cliente"]["nome"],
                    pedido_data["cliente"]["email"],
                    pedido_data["cliente"]["cpf"],
                ),
                itens=[
                    Item(id=item["id"], nome=item["nome"], preco=item["preco"])
                    for item in pedido_data["itens"]
                ],
                status=pedido_data["status"],
            )
        raise DocumentNotFoundError(f"Pedido com id {id} não encontrado.")

    def listar_todos(self) -> List[Pedido]:
        pedidos = self.collection.find()

        return [
            Pedido(
                id=pedido["_id"],
                cliente=Cliente(**pedido["cliente"]),
                itens=[
                    Item(id=item["id"], nome=item["nome"], preco=item["preco"])
                    for item in pedido["itens"]
                ],
                status=pedido["status"],
            )
            for pedido in pedidos
        ]
