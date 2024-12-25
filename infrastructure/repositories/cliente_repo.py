from core.entities.cliente import Cliente
from core.repositories.cliente_repo import ClienteRepository as ClienteRepo
from infrastructure.database.mongo_connection import get_mongo_client


class ClienteRepository(ClienteRepo):
    def __init__(self, db=None):
        if db is None:
            client = get_mongo_client()
            db = client["lanchonete"]
        self.collection = db["clientes"]

    def salvar(self, cliente: Cliente) -> None:
        self.db["clientes"].insert_one(
            {
                "_id": cliente.id,
                "nome": cliente.nome,
                "email": cliente.email,
                "cpf": cliente.cpf,
            }
        )

    def buscar_por_id(self, id: str):
        return self.db["clientes"].find_one({"_id": id})
