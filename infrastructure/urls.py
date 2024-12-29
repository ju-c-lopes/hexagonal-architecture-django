from django.urls import path
from infrastructure.views.cliente_view import ClienteAPIView

urlpatterns = [
    path('clientes/<int:id>/', ClienteAPIView.as_view(), name='cliente-detail'),
    path('clientes/', ClienteAPIView.as_view(), name='cliente-list'),
]
