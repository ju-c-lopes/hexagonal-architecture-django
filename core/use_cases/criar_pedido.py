from core.entities.cliente import Cliente
from core.entities.item import Item
from core.entities.pedido import Pedido
from core.repositories.cliente_repo import ClienteRepository
from core.repositories.pedido_repo import PedidoRepository
from infrastructure.exceptions import DocumentNotFoundError


class CriarPedido:
    def __init__(
        self, pedido_repository: PedidoRepository, cliente_repository: ClienteRepository
    ):
        self.pedido_repository = pedido_repository
        self.cliente_repository = cliente_repository

    def execute(self, cliente_data, itens, status="PENDENTE", id=None) -> Pedido:
        # Verificar se o cliente já existe
        try:
            cliente = self.cliente_repository.buscar_por_id(str(cliente_data.id))

        except DocumentNotFoundError:
            cliente = Cliente(
                id=cliente_data.id,
                nome=cliente_data.nome,
                email=cliente_data.email,
                cpf=cliente_data.cpf,
            )

        # Criar instância de Pedido
        pedido = Pedido(
            id=id if id is not None else None,
            cliente=cliente,
            itens=[Item(**item) for item in itens],
            status=status,
        )

        # Salvar pedido no repositório
        self.pedido_repository.salvar(pedido)

        return pedido
