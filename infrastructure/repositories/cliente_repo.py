from adapters.driven.database.mongo_connection import get_mongo_client
from core.entities.cliente import Cliente
from core.repositories.cliente_repo import ClienteRepository as ClienteRepo
from infrastructure.exceptions import DocumentNotFoundError
from infrastructure.serializers import ClienteSerializer


class ClienteRepository(ClienteRepo):
    def __init__(self, db=None):
        if db is None:
            client = get_mongo_client()
            db = client["lanchonete"]
        self.collection = db["clientes"]

    def salvar(self, cliente: Cliente) -> None:
        self.collection.insert_one(
            {
                "nome": cliente.nome,
                "email": cliente.email,
                "cpf": cliente.cpf,
            }
        )

    def buscar_por_cpf(self, cpf: str):
        data = self.collection.find_one({"cpf": cpf})
        if data is None:
            raise DocumentNotFoundError(f"Cliente com CPF {cpf} não encontrado")
        return ClienteSerializer(data)
        # Cliente(
        #     id=data["_id"],
        #     nome=data["nome"],
        #     email=data["email"],
        #     cpf=data["cpf"],
        # )

    def listar_todos(self):
        clientes = []
        for data in self.collection.find():
            clientes.append(
                Cliente(
                    id=data["_id"],
                    nome=data["nome"],
                    email=data["email"],
                    cpf=data["cpf"],
                )
            )
        return clientes
