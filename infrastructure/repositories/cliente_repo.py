from core.entities.cliente import Cliente
from core.repositories.cliente_repo import ClienteRepository as ClienteRepo
from infrastructure.database.mongo_connection import get_mongo_client
from infrastructure.exceptions import DocumentNotFoundError


class ClienteRepository(ClienteRepo):
    def __init__(self, db=None):
        if db is None:
            db = get_mongo_client()
        self.collection = db["lanchonete"]["clientes"]

    def salvar(self, cliente: Cliente) -> None:
        self.db["lanchonete"]["clientes"].insert_one(
            {
                "_id": cliente.id,
                "nome": cliente.nome,
                "email": cliente.email,
                "cpf": cliente.cpf,
            }
        )

    def buscar_por_id(self, id: str):
        data = self.collection.find_one({"id": id})
        if data is None:
            raise DocumentNotFoundError(f"Cliente com ID {id} não encontrado")
        return Cliente(
            id=data["id"],
            nome=data["nome"],
            email=data["email"],
            cpf=data["cpf"],
        )

    def listar_todos(self):
        clientes = []
        for data in self.collection.find():
            clientes.append(
                Cliente(
                    id=data["id"],
                    nome=data["nome"],
                    email=data["email"],
                    cpf=data["cpf"],
                )
            )
        return clientes
