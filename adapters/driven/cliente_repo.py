from bson import ObjectId

from adapters.driven.database.mongo_connection import get_mongo_client
from core.entities.cliente import Cliente
from core.repositories.cliente_repo import ClienteRepository as ClienteRepo
from infrastructure.exceptions import DocumentNotFoundError


class ClienteRepository(ClienteRepo):
    COLLECTION_NAME = "clientes"  # Define the collection name as a class constant
    DATABASE_NAME = "lanchonete"  # Define the database name as a class constant

    def __init__(self, db=None):
        """Initialize repository with a MongoDB client."""
        self.db = db or get_mongo_client()
        self.collection = self.db[self.DATABASE_NAME][self.COLLECTION_NAME]

    def _buscar_por_criterio(self, criterio: dict) -> Cliente:
        """Helper method to find a client based on a given criterion (e.g., id or cpf)."""
        data = self.collection.find_one(criterio)
        if data is None:
            raise DocumentNotFoundError(f"Cliente com dados {criterio} não encontrado.")
        return data

    def salvar(self, cliente: Cliente) -> Cliente:
        """Save a new client to the database."""
        cliente_data = {
            "nome": cliente.nome,
            "email": cliente.email,
            "cpf": cliente.cpf,
        }
        result = self.collection.insert_one(cliente_data)
        cliente.id = result.inserted_id  # Set the id from MongoDB
        return cliente

    def buscar_por_id(self, id: str) -> Cliente:
        """Find a client by their ID."""
        obj_id = ObjectId(id)
        return self._buscar_por_criterio({"_id": obj_id})

    def buscar_por_cpf(self, cpf: str) -> Cliente:
        """Find a client by their CPF."""
        return self._buscar_por_criterio({"cpf": cpf})

    def listar_todos(self) -> list[Cliente]:
        """List all clients."""
        return [cliente for cliente in self.collection.find()]
