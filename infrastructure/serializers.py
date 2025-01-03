from rest_framework import serializers

from core.entities.cliente import Cliente


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)
    preco = serializers.FloatField()


class ClienteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=11 | 12)

    def create(self, validated_data):
        return Cliente(**validated_data)


class PedidoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cliente = ClienteSerializer()
    itens = ItemSerializer(many=True)
    total = serializers.FloatField()
    status = serializers.CharField(max_length=20)
