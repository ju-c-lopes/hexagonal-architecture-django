from core.entities.cliente import Cliente
from core.entities.pedido import Pedido
from core.repositories.cliente_repo import ClienteRepository
from core.repositories.pedido_repo import PedidoRepository


class CriarPedido:
    def __init__(
        self, pedido_repository: PedidoRepository, cliente_repository: ClienteRepository
    ):
        self.pedido_repository = pedido_repository
        self.cliente_repository = cliente_repository

    def execute(self, cliente_data, itens):
        # Verificar se o cliente já existe

        cliente = self.cliente_repository.buscar_por_id(cliente_data.id)
        if not isinstance(cliente, Cliente):
            # Criar novo cliente
            cliente = Cliente(
                id=cliente_data.id,
                nome=cliente_data.nome,
                email=cliente_data.email,
                cpf=cliente_data.cpf,
            )

        # Criar instância de Pedido
        pedido = Pedido(
            id=self.pedido_repository.get_next_id(),
            cliente=cliente,
            itens=itens,
        )

        # Salvar pedido no repositório
        self.pedido_repository.salvar(pedido)

        return pedido
