from rest_framework import serializers

from core.entities.cliente import Cliente
from core.entities.item import Item
from core.entities.pedido import Pedido


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)
    preco = serializers.FloatField()

    def create(self, validated_data):
        return Item(**validated_data)

    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.preco = validated_data.get('preco', instance.preco)
        return instance


class ClienteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=11 | 12)

    def create(self, validated_data):
        return Cliente(**validated_data)

    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.email = validated_data.get('email', instance.email)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        return instance


class PedidoSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    cliente = ClienteSerializer()
    itens = ItemSerializer(many=True)
    status = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Pedido(**validated_data)

    def update(self, instance, validated_data):
        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.itens = validated_data.get('itens', instance.itens)
        instance.status = validated_data.get('status', instance.status)
        return instance
