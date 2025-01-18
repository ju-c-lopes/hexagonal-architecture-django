from datetime import datetime

from core.entities.pedido import Pedido
from core.repositories.cliente_repo import ClienteRepository
from core.repositories.pedido_repo import PedidoRepository
from core.services.contador_codigo_pedido import ContadorDiario
from infrastructure.exceptions import DocumentNotFoundError


class CriarPedido:
    def __init__(
        self, pedido_repository: PedidoRepository, cliente_repository: ClienteRepository
    ):
        self.pedido_repository = pedido_repository
        self.cliente_repository = cliente_repository
        self.contador_diario = ContadorDiario()

    def execute(self, produtos, cliente_data=None, status="PENDENTE", personalizacao=None) -> Pedido:
        # Verificar se o cliente já existe
        cliente = None
        if cliente_data:
            try:
                cliente = self.cliente_repository.buscar_por_cpf(str(cliente_data["cpf"]))
            except DocumentNotFoundError:
                cliente = cliente_data

        # Gerar o código do pedido com base na data e no contador
        data_atual = datetime.now().strftime("%Y%m%d")
        numero_sequencial = self.contador_diario.obter_proximo()
        codigo_pedido = f"{data_atual}-{numero_sequencial:03d}"

        # Criar instância de Pedido
        pedido = Pedido(
            cliente=cliente if cliente else None,
            produtos=[produto for produto in produtos],
            personalizacao=personalizacao,
            codigo_do_pedido=codigo_pedido,
            status="Aguardando pagamento...",
        )
        pedido.cadastro = pedido.set_cadastro()
        pedido.total = pedido.calcular_total()

        # Salvar pedido no repositório
        self.pedido_repository.salvar(pedido)

        return pedido
