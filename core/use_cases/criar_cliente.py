from adapters.driven.cliente_repo import ClienteRepository
from core.entities.cliente import Cliente
from infrastructure.serializers import ClienteSerializer


class CriarCliente:
    def __init__(self):
        self.cliente_repo = ClienteRepository()

    def executar(self, cliente_data, id=None) -> Cliente:

        serializer = ClienteSerializer(data=cliente_data)
        if serializer.is_valid():
            cliente = Cliente(
            id=None,
            nome=serializer.validated_data["nome"],
            email=serializer.validated_data["email"],
            cpf=serializer.validated_data["cpf"],
            )
            data = self.cliente_repo.salvar(cliente)
            return data
        return None
        
