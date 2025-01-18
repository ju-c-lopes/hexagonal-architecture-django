from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from adapters.driven.cliente_repo import ClienteRepository
from core.use_cases.criar_pedido import CriarPedido
from core.use_cases.listar_pedido import ListarPedido
from core.use_cases.listar_pedidos import ListarPedidos
from core.use_cases.listar_produtos import ListarProdutosUseCase
from infrastructure.exceptions import DocumentNotFoundError
from infrastructure.repositories.pedido_repo import PedidoRepository
from infrastructure.repositories.produtos_repo import ProdutosRepository
from infrastructure.serializers import PedidoSerializer


class ProdutosMenu:
    """
    A class used to represent the menu of products.
    Methods
    -------
    __init__():
        Initializes the ProdutosMenu with a ProdutosRepository and ListarProdutosUseCase.
    execute():
        Executes the use case to list products and organizes them into menus.
        Returns a list of menus where each menu contains a product category and its items.
    """
    def __init__(self):
        self.produtos_repo = ProdutosRepository()
        self.listar_produtos = ListarProdutosUseCase(self.produtos_repo)

    def execute(self):
        produtos = self.listar_produtos.execute()
        if len(produtos) > 0:
            print('Menus de produtos:')
            menus = [[produtos[0][0], produtos[0][1]]]
            j = 0
            for i in range(1, len(produtos)):
                if produtos[i - 1][0] == produtos[i][0]:
                    menus[j][1] += f"\n{produtos[i][1]}"
                else:
                    menus.append(list(produtos[i]))
                    j += 1
            return [menu for menu in menus]
        return False


class PedidoPorCodigoAPIView(APIView):
    """
    API para buscar um pedido pelo código do pedido.

    Métodos:
    - GET /pedidos/<str:codigo_do_pedido>/ : Detalhes de um pedido pelo codigo do pedido.
    """

    def __init__(self, pedido_repo=None, **kwargs):
        super().__init__(**kwargs)
        self.pedido_repo = pedido_repo or PedidoRepository()
        self.listar_pedido = ListarPedido(self.pedido_repo)

    def get(self, request, codigo_do_pedido):
        try:
            pedido = self.listar_pedido.execute(codigo_do_pedido)
        except DocumentNotFoundError:
            return Response(
                {"error": "Pedido não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)


class PedidoAPIView(APIView):
    """
    API para gerenciamento de pedidos.

    Métodos:
    - GET /pedidos/ : Lista todos os pedidos.
    - POST /pedidos/ : Criação de um novo pedido.
    """

    def __init__(
        self, pedido_repo=None, cliente_repo=None, produtos_repo=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.pedido_repo = pedido_repo or PedidoRepository()
        self.cliente_repo = cliente_repo or ClienteRepository()
        self.produtos_repo = produtos_repo or ProdutosRepository()
        self.listar_produtos = ListarProdutosUseCase(self.produtos_repo)
        self.listar_pedidos = ListarPedidos(self.pedido_repo)
        self.listar_pedido = ListarPedido(self.pedido_repo)
        self.criar_pedido = CriarPedido(self.pedido_repo, self.cliente_repo)

    def get(self, request):
        pedido = self.listar_pedidos.execute()
        serializer = PedidoSerializer(pedido, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "CPF do Cliente",
                openapi.IN_QUERY,  # Define como query param
                description="Insira seu CPF para fazer o pedido",
                type=openapi.TYPE_STRING,
            ),
            # Campos de LANCHE
            openapi.Parameter(
                ProdutosMenu().execute()[0][0] if ProdutosMenu().execute() else "LANCHE",
                openapi.IN_QUERY,  # Define como query param
                description=ProdutosMenu().execute()[0][1] if ProdutosMenu().execute() else "",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "OBSERVACAO:",
                openapi.IN_QUERY,
                description="ex: sem tomate...",
                type=openapi.TYPE_STRING,
            ),
            # Campos de ACOMPANHAMENTO
            openapi.Parameter(
                ProdutosMenu().execute()[1][0] if ProdutosMenu().execute() else "ACOMPANHAMENTO",
                openapi.IN_QUERY,
                description=ProdutosMenu().execute()[1][1] if ProdutosMenu().execute() else "",
                type=openapi.TYPE_STRING,
            ),
            # Campos de BEBIDA
            openapi.Parameter(
                ProdutosMenu().execute()[2][0] if ProdutosMenu().execute() else "BEBIDA",
                openapi.IN_QUERY,
                description=ProdutosMenu().execute()[2][1] if ProdutosMenu().execute() else "",
                type=openapi.TYPE_STRING,
            ),
            # Campos de SOBREMESA
            openapi.Parameter(
                ProdutosMenu().execute()[3][0] if ProdutosMenu().execute() else "SOBREMESA",
                openapi.IN_QUERY,
                description=ProdutosMenu().execute()[3][1] if ProdutosMenu().execute() else "",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(description="Pedido criado com sucesso"),
            400: openapi.Response(description="Erro ao criar pedido"),
        },
    )
    def post(self, request):
        cliente_cpf = request.query_params.get("CPF do Cliente")
        cliente_data = None
        if cliente_cpf:
            cliente_data = self.cliente_repo.buscar_por_cpf(cliente_cpf)
            if not cliente_data:
                return Response(
                    {"error": "Cliente não encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        dados_do_pedido = {
            "LANCHE": request.query_params.get("LANCHE", None),
            "Personalizacao": request.query_params.get("OBSERVACAO:", None),
            "ACOMPANHAMENTO": request.query_params.get("ACOMPANHAMENTO", None),
            "BEBIDA": request.query_params.get("BEBIDA", None),
            "SOBREMESA": request.query_params.get("SOBREMESA", None),
        }

        montagem_do_pedido = self.listar_produtos.montar_pedido(dados_do_pedido, cliente_data)

        if montagem_do_pedido is None:
            return Response(
                {"message": "Nenhum produto cadastrado no sistema. Talvez precise cadastrar alguns produtos antes de iniciar os pedidos."},
                status=status.HTTP_404_NOT_FOUND,
            )
        pedido = self.criar_pedido.execute(
            cliente_data=montagem_do_pedido.cliente if montagem_do_pedido
            .cliente else None,
            produtos=montagem_do_pedido.produtos,
            personalizacao=montagem_do_pedido.personalizacao,
        )

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
