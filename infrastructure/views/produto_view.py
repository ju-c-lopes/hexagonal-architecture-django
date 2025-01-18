from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.repositories.produtos_repo import ProdutosRepository
from infrastructure.serializers import ProdutoSerializer


class ProdutoListCreateAPIView(APIView):
    """
    API para listar e criar produtos.

    Métodos:
    - GET /produtos/ : Lista todos os produtos.
    - POST /produtos/ : Criação de um novo produto.
    """

    def __init__(self, produtos_repo=None, **kwargs):
        super().__init__(**kwargs)
        self.produtos_repo = produtos_repo or ProdutosRepository()

    def get(self, request):
        produtos = self.produtos_repo.listar_todos()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProdutoSerializer, operation_description="não precisa informar id"
    )
    def post(self, request):
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            self.produtos_repo.cadastrar_produto(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProdutoDeleteAPIView(APIView):
    """
    API para excluir produtos.

    Métodos:
    - DELETE /produtos/excluir/<str:produto_id>/ : Excluir um produto pelo ID.
    """

    def __init__(self, produtos_repo=None, **kwargs):
        super().__init__(**kwargs)
        self.produtos_repo = produtos_repo or ProdutosRepository()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'produto_id',
                openapi.IN_PATH,
                description="ID do produto a ser excluído",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
        operation_description="Excluir um produto pelo ID"
    )
    def delete(self, request, produto_id, format=None):
        if self.produtos_repo.excluir_produto_por_id(produto_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProdutoUpdateAPIView(APIView):
    """
    API para atualizar produtos.

    Métodos:
    - PUT /produtos/atualizar/<str:produto_id>/ : Atualizar um produto pelo ID.
    """

    def __init__(self, produtos_repo=None, **kwargs):
        super().__init__(**kwargs)
        self.produtos_repo = produtos_repo or ProdutosRepository()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'produto_id',
                openapi.IN_PATH,
                description="ID do produto a ser atualizado",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome': openapi.Schema(type=openapi.TYPE_STRING),
                'descricao': openapi.Schema(type=openapi.TYPE_STRING),
                'categoria': openapi.Schema(type=openapi.TYPE_STRING),
                'preco': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        ),
        responses={
            200: 'OK',
            404: 'Not Found'
        },
        operation_description="Atualizar um produto pelo ID"
    )
    def put(self, request, produto_id, format=None):
        produto_atualizado = request.data
        modified_count = self.produtos_repo.atualizar_produto(produto_id, produto_atualizado)
        if modified_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class ProdutoCategoriaAPIView(APIView):
    """
    API para listar produtos por categoria.

    Métodos:
    - GET /produtos/<str:categoria>/ : Lista produtos por categoria.
    """

    def __init__(self, produtos_repo=None, **kwargs):
        super().__init__(**kwargs)
        self.produtos_repo = produtos_repo or ProdutosRepository()

    def get(self, request, categoria):
        produtos = self.produtos_repo.listar_por_categoria(categoria)
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
