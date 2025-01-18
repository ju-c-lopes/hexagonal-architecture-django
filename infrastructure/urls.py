from django.urls import path

from adapters.driver.cliente_view import ClienteAPIView, ClienteDetalheAPIView
from infrastructure.views.pagamento_view import PagamentoAPIView, PagamentoDetalheAPIView
from infrastructure.views.pedido_view import PedidoAPIView, PedidoPorCodigoAPIView

from .views.produto_view import (
    ProdutoCategoriaAPIView,
    ProdutoDeleteAPIView,
    ProdutoListCreateAPIView,
    ProdutoUpdateAPIView,
)

urlpatterns = [
    path("clientes/<str:cpf>/", ClienteDetalheAPIView.as_view(), name="cliente-detail"),
    path("clientes/", ClienteAPIView.as_view(), name="cliente-list"),
    path("produtos/", ProdutoListCreateAPIView.as_view(), name="produtos"),
    path(
        "produtos/<str:categoria>/",
        ProdutoCategoriaAPIView.as_view(),
        name="produtos_por_categoria",
    ),
    path(
        "produtos/excluir/<str:produto_id>/",
        ProdutoDeleteAPIView.as_view(),
        name="excluir_produto",
    ),
    path(
        "produtos/atualizar/<str:produto_id>/",
        ProdutoUpdateAPIView.as_view(),
        name="atualizar_produto",
    ),
    path(
        "pedidos/<str:codigo_do_pedido>/",
        PedidoPorCodigoAPIView.as_view(),
        name="pedido-detail",
    ),
    path("pedidos/", PedidoAPIView.as_view(), name="pedido-list"),
    path("pagamento/", PagamentoAPIView.as_view(), name="pagamento"),
    path("pagamento/<str:codigo_do_pedido>/", PagamentoDetalheAPIView.as_view(), name="pagamento-detail"),

]
