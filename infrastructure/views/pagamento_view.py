from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.exceptions import DocumentNotFoundError
from infrastructure.serializers import PagamentoSerializer
from infrastructure.services.pagamento_api import Pagamento


class PagamentoAPIView(APIView):
    """
    API para fazer pagamento de um pedido com "Fake Checkout"

    Métodos:
    - POST /pagamentos/ : Criação de um novo pagamento.
    - GET /pagamentos/ : Lista todos os pagamentos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pagamento = Pagamento()

    @swagger_auto_schema(
        request_body=PagamentoSerializer,
        operation_description="não precisa informar id",
    )
    def post(self, request):
        pedido = self.pagamento.buscarPedido(request.data.get("codigo_do_pedido"))

        # Atualizar o status do pedido
        pedido["status"] = "Pago"
        self.pagamento.atualizarPedido(pedido["codigo_do_pedido"], pedido)

        pagamento = self.pagamento.checkout(pedido)
        self.pagamento.salvar_pagamento(pagamento)
        return Response(pagamento, status=status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(
        operation_summary="Listar todos os pagamentos",
        operation_description="Recupera todos os pagamentos.",
        responses={
            200: PagamentoSerializer(many=True),
        },
    )
    def get(self, request):
        pagamentos = self.pagamento.listarTodos()
        pagamentos = [PagamentoSerializer(pagamento).data for pagamento in pagamentos]
        return Response(pagamentos, status=status.HTTP_200_OK)


class PagamentoDetalheAPIView(APIView):
    """
    API para buscar um pagamento pelo código do pedido.

    Métodos:
    - GET /pagamentos/<str:codigo_do_pedido>/ : Recupera um pagamento pelo código do pedido.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pagamento = Pagamento()

    @swagger_auto_schema(
        operation_summary="Recuperar um pagamento",
        operation_description="Recupera um pagamento por código do pedido.",
        manual_parameters=[
            openapi.Parameter(
                "codigo_do_pedido",
                openapi.IN_PATH,
                description="Código do pedido",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: PagamentoSerializer,
            404: openapi.Response("Pagamento não encontrado"),
        },
    )
    def get(self, request, codigo_do_pedido):
        try:
            pagamento = self.pagamento.buscarPagamentoPorCodigo(codigo_do_pedido)
            pagamento = PagamentoSerializer(pagamento).data
            return Response(pagamento, status=status.HTTP_200_OK)
        except DocumentNotFoundError:
            return Response(
                {"error": "Pagamento não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
