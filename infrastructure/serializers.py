from rest_framework import serializers
from rest_framework.fields import ChoiceField

from core.entities.cliente import Cliente
from core.entities.pedido import Pedido
from core.entities.produto import Categoria, Produto
from infrastructure.services.pagamento_api import Pagamento as Pagto


class CategoriaField(ChoiceField):
    def __init__(self, **kwargs):
        self.enum_class = Categoria
        choices = [(tag.name, tag.value) for tag in self.enum_class]
        super().__init__(choices=choices, **kwargs)

    def to_representation(self, obj):
        if isinstance(obj, self.enum_class):
            return obj.name
        return super().to_representation(obj)

    def to_internal_value(self, data):
        for tag in self.enum_class:

            if tag.name == data:
                return tag.name
            if isinstance(data, Categoria) and data.name == tag.name:
                return tag.name
        raise ValueError(f"Valor inválido para Categoria: {data}")


class ProdutoSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=36, required=False)
    nome = serializers.CharField(max_length=100)
    descricao = serializers.CharField(max_length=255)
    categoria = CategoriaField()
    preco = serializers.FloatField()

    def create(self, validated_data):

        return Produto(**validated_data)

    def update(self, instance, validated_data):
        instance.nome = validated_data.get("nome", instance.nome)
        instance.descricao = validated_data.get("descricao", instance.descricao)
        instance.categoria = validated_data.get("categoria", instance.categoria)
        instance.preco = validated_data.get("preco", instance.preco)
        return instance


class ClienteSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=36, required=False)
    nome = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=11 | 12)

    def create(self, validated_data):
        return Cliente(**validated_data)

    def update(self, instance, validated_data):
        instance.nome = validated_data.get("nome", instance.nome)
        instance.email = validated_data.get("email", instance.email)
        instance.cpf = validated_data.get("cpf", instance.cpf)
        return instance


class PedidoSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=36, required=False)
    cliente = ClienteSerializer(required=False)
    produtos = ProdutoSerializer(many=True)
    personalizacao = serializers.CharField(max_length=255, required=False)
    codigo_do_pedido = serializers.CharField(max_length=12, required=False)
    status = serializers.CharField(max_length=20)
    total = serializers.FloatField(required=False)

    def create(self, validated_data):
        return Pedido(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.cliente = validated_data.get("cliente", instance.cliente)
        instance.produtos = validated_data.get("produtos", instance.produtos)
        instance.codigo_do_pedido = validated_data.get("codigo_do_pedido", instance.codigo_do_pedido)
        instance.status = validated_data.get("status", instance.status)
        instance.total = validated_data.get("total", instance.total)
        return instance


class PagamentoSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=36, required=False)
    codigo_do_pedido = serializers.CharField(max_length=12)
    mensagem = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Pagto(**validated_data)

    def update(self, instance, validated_data):
        instance._id = validated_data.get("_id", instance.id)
        instance.codigo_do_pedido = validated_data.get("codigo_do_pedido", instance.codigo_do_pedido)
        instance.mensagem = validated_data.get("mensagem", instance.mensagem)
        return instance
