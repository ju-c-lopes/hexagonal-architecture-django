from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.entities.cliente import Cliente
from infrastructure.exceptions import DocumentNotFoundError
from infrastructure.repositories.cliente_repo import ClienteRepository
from infrastructure.serializers import ClienteSerializer


class ClienteAPIView(APIView):
    def __init__(self, cliente_repo=None, **kwargs):
        super().__init__(**kwargs)
        self.cliente_repo = (
            cliente_repo if cliente_repo is not None else ClienteRepository()
        )

    def get(self, request, id=None):
        if id:
            # Buscar cliente específico
            cliente = self.cliente_repo.buscar_por_id(id)
            if not cliente:
                raise DocumentNotFoundError(f"Cliente com ID {id} não encontrado")
            serializer = ClienteSerializer(cliente)
            return Response(serializer.data)
        else:
            # Listar todos os clientes
            clientes = self.cliente_repo.listar_todos()
            serializer = ClienteSerializer(clientes, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = Cliente(
                id=None,
                nome=serializer.validated_data["nome"],
                email=serializer.validated_data["email"],
                cpf=serializer.validated_data["cpf"],
            )
            self.cliente_repo.salvar(cliente)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
