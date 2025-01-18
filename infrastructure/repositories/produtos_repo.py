from adapters.driven.database.mongo_connection import get_mongo_client
from core.entities.produto import Produto
from core.repositories.produtos_repo import ProdutosRepository as ProdutosRepo
from bson import ObjectId


class ProdutosRepository(ProdutosRepo):
    def __init__(self, db=None):
        if db is None:
            client = get_mongo_client()
            db = client["lanchonete"]
        self.collection = db["produtos"]

    def cadastrar_produto(self, produto: Produto):

        novo_produto = {
            "nome": produto["nome"],
            "descricao": produto["descricao"],
            "categoria": produto["categoria"],
            "preco": produto["preco"],
        }
        self.collection.insert_one(novo_produto)

    def listar_todos(self):
        produtos = self.collection.find()
        return [
            Produto(
                id=produto["_id"],
                nome=produto["nome"],
                descricao=produto["descricao"],
                categoria=produto["categoria"],
                preco=produto["preco"],
            )
            for produto in produtos
        ]

    def listar_por_categoria(self, categoria):
        produtos = self.collection.find({"categoria": categoria})

        return [
            Produto(
                id=produto["_id"],
                nome=produto["nome"],
                descricao=produto["descricao"],
                categoria=produto["categoria"],
                preco=produto["preco"],
            )
            for produto in produtos
        ]

    def excluir_produto_por_id(self, produto_id):
        result = self.collection.delete_one({"_id": ObjectId(produto_id)})
        return result.deleted_count

    def atualizar_produto(self, produto_id, produto_atualizado: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(produto_id)},
            {"$set": produto_atualizado}
        )
        return result.modified_count