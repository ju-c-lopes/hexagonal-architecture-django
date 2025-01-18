from core.entities.pedido import Pedido
from core.use_cases.criar_pedido import CriarPedido


class IniciarPedidoUseCase:
    def __init__(self):
        self.pedido = CriarPedido()

    def execute(self, cliente=None, produtos=None) -> Pedido:
        # Validação de produtos
        if not produtos or len(produtos) == 0:
            raise ValueError("O pedido deve conter ao menos um produto.")

        # Criar pedido
        self.pedido.execute(
            id=None,
            cliente_data=cliente,
            produtos=produtos,
            status="Iniciado",
        )

        return self.pedido
