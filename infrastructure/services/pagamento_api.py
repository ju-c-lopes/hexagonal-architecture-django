import time

from adapters.driven.database.mongo_connection import get_mongo_client
from infrastructure.exceptions import DocumentNotFoundError


class Pagamento:
    def __init__(self, pedido=None, db=None):
        if db is None:
            client = get_mongo_client()
            db = client["lanchonete"]
        self.collection = db["pedidos"]
        self.pagamentos_collection = db["pagamentos"]
        self.codigo__do_pedido = None
        self.pedido = pedido
        self.mensagem = None

    def buscarPedido(self, codigo_do_pedido: str):
        if not isinstance(codigo_do_pedido, str):
            raise ValueError("O código do pedido deve ser uma string.")

        # Realize a consulta no MongoDB
        pedido = self.collection.find_one({"codigo_do_pedido": codigo_do_pedido})

        if pedido is None:
            raise DocumentNotFoundError(
                f"Pedido com código {codigo_do_pedido} não encontrado."
            )

        return pedido

    def atualizarPedido(self, codigo_do_pedido: str, pedido_atualizado):
        self.collection.update_one(
            {"codigo_do_pedido": codigo_do_pedido},
            {"$set": pedido_atualizado}
        )

    def checkout(self, pedido):
        total = pedido.get("total", 0.0)
        print(f'Total do pedido: R$ {total:.2f}')
        print(f'Processando pagamento do pedido {pedido["codigo_do_pedido"]}')
        time.sleep(10)
        mensagem = f'O pedido {pedido["codigo_do_pedido"]} foi pago com R$ {total:.2f}'
        self.codigo__do_pedido = pedido["codigo_do_pedido"]
        return {"codigo_do_pedido": pedido["codigo_do_pedido"], "mensagem": mensagem}

    def salvar_pagamento(self, pagamento):
        from infrastructure.serializers import PagamentoSerializer
        serializer = PagamentoSerializer(data=pagamento)
        if serializer.is_valid():
            self.pagamentos_collection.insert_one(serializer.data)

    def listarTodos(self):
        pagamentos = self.pagamentos_collection.find()
        return list(pagamentos)

    def buscarPagamentoPorCodigo(self, codigo_do_pedido: str):
        pagamento = self.pagamentos_collection.find_one({"codigo_do_pedido": codigo_do_pedido})
        if pagamento is None:
            raise DocumentNotFoundError(
                f"Pagamento com código do pedido {codigo_do_pedido} não encontrado."
            )
        return pagamento
