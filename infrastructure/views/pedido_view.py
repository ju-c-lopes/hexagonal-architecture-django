from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.entities.cliente import Cliente
from core.use_cases.criar_pedido import CriarPedido
from core.use_cases.listar_pedido import ListarPedido
from core.use_cases.listar_pedidos import ListarPedidos
from infrastructure.exceptions import DocumentNotFoundError
from infrastructure.repositories.cliente_repo import ClienteRepository
from infrastructure.repositories.pedido_repo import PedidoRepository
from infrastructure.serializers import PedidoSerializer


class PedidoAPIView(APIView):
    def __init__(self, pedido_repo=None, cliente_repo=None, **kwargs):
        super().__init__(**kwargs)
        self.pedido_repo = pedido_repo or PedidoRepository()
        self.cliente_repo = cliente_repo or ClienteRepository()
        self.criar_pedido = CriarPedido(self.pedido_repo, self.cliente_repo)
        self.listar_pedidos = ListarPedidos(self.pedido_repo)
        self.listar_pedido = ListarPedido(self.pedido_repo)

    def get(self, request, id=None):
        if id:
            try:
                pedido = self.listar_pedido.execute(id)
            except DocumentNotFoundError:
                return Response(
                    {"error": "Pedido não encontrado"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = PedidoSerializer(pedido)
            return Response(serializer.data)
        else:
            pedidos = self.listar_pedidos.execute()
            serializer = PedidoSerializer(pedidos, many=True)

            return Response(serializer.data)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            # Usar o caso de uso para criar o pedido
            self.criar_pedido.execute(
                cliente_data=Cliente(
                    serializer.validated_data["cliente"]["id"],
                    serializer.validated_data["cliente"]["nome"],
                    serializer.validated_data["cliente"]["email"],
                    serializer.validated_data["cliente"]["cpf"],
                ),
                itens=serializer.validated_data["itens"],
                status=serializer.validated_data["status"],
                id=serializer.validated_data.get("id"),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
