from django.urls import path
from infrastructure.views.cliente_view import ClienteAPIView
from infrastructure.views.pedido_view import PedidoAPIView

urlpatterns = [
    path('clientes/<int:id>/', ClienteAPIView.as_view(), name='cliente-detail'),
    path('clientes/', ClienteAPIView.as_view(), name='cliente-list'),
    path('pedidos/<str:id>/', PedidoAPIView.as_view(), name='pedido-detail'),
    path('pedidos/', PedidoAPIView.as_view(), name='pedido-list'),
]
