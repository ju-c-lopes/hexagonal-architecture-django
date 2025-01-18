from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from infrastructure.serializers import ClienteSerializer
from core.use_cases.criar_cliente import CriarCliente
from core.use_cases.listar_cliente import ListarCliente


class ClienteAPIView(APIView):

    def __init__(self, listar_cliente_use_case=None, criar_cliente_use_case=None, **kwargs):
        super().__init__(**kwargs)
        self.listar_clientes_use_case = (
            listar_cliente_use_case if listar_cliente_use_case is not None else ListarCliente()
        )
        self.criar_cliente_use_case = (
            criar_cliente_use_case if criar_cliente_use_case is not None else CriarCliente()
        )

    @swagger_auto_schema(
        operation_summary="Recuperar todos os clientes",
        operation_description="Recuperar todos os clientes.",
        responses={
            200: openapi.Response("Successo", ClienteSerializer(many=True)),
        },
    )
    def get(self, request):
        clientes = self.listar_clientes_use_case.executar()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Cadastrar um novo cliente",
        operation_description="Cadastra um novo cliente com os dados informados.",
        request_body=ClienteSerializer,
        responses={
            201: ClienteSerializer,
            400: openapi.Response("Dados inválidos"),
        },
    )
    def post(self, request):
        """Criar um novo cliente"""
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = self.criar_cliente_use_case.executar(serializer.validated_data)
            return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteDetalheAPIView(APIView):
    """
    API para gerenciamento de clientes.

    Métodos:
    - GET /clientes/<str:cpf>/ : Detalhes de um cliente pelo CPF.
    - GET /clientes/ : Lista todos os clientes.
    - POST /clientes/ : Criação de um novo cliente.
    """
    def __init__(self, listar_cliente_use_case=None, **kwargs):
        super().__init__(**kwargs)
        self.listar_clientes_use_case = (
            listar_cliente_use_case if listar_cliente_use_case is not None else ListarCliente()
        )

    @swagger_auto_schema(
        operation_summary="Recuperar um cliente",
        operation_description="Recupera um cliente por CPF.",
        manual_parameters=[
            openapi.Parameter(
                "cpf",
                openapi.IN_PATH,
                description="CPF do cliente",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response("SuccessO", ClienteSerializer),
            404: openapi.Response("Cliente não encontrado"),
        },
    )
    def get(self, request, cpf):
        """Fetch a client by CPF"""
        try:
            cliente = self.listar_clientes_use_case.executar(cpf)
            return Response(ClienteSerializer(cliente).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
