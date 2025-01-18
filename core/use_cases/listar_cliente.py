from adapters.driven.cliente_repo import ClienteRepository
from infrastructure.exceptions import DocumentNotFoundError
from infrastructure.serializers import ClienteSerializer


class ListarCliente:
    def __init__(self):
        self.cliente_repo = ClienteRepository()

    def executar(self, identifier=None):
        if identifier:
            cliente = self._buscar_cliente_por_cpf(identifier)
            
            if not cliente:
                raise DocumentNotFoundError(f"Cliente com identificador {identifier} não encontrado")
            
            serializer = ClienteSerializer(cliente)
            return serializer.data
        else:
            # List all clients
            clientes = self.cliente_repo.listar_todos()
            serializer = ClienteSerializer(clientes, many=True)
            return serializer.data

    def _buscar_cliente_por_id(self, id):
        """Helper method to search for a client by id"""
        try:
            cliente = self.cliente_repo.buscar_por_id(id)
            return cliente
        except DocumentNotFoundError:
            return None  # Return None if not found

    def _buscar_cliente_por_cpf(self, cpf):
        """Helper method to search for a client by cpf"""
        try:
            cliente = self.cliente_repo.buscar_por_cpf(cpf)
            return cliente
        except DocumentNotFoundError:
            return None  # Return None if not found
