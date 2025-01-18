from core.entities.produto import Produto
from core.repositories.produtos_repo import ProdutosRepository


class CadastrarProdutoUseCase:
    def __init__(self, produtos_repository: ProdutosRepository):
        self.produtos_repository = produtos_repository

    def execute(self, nome, descricao, categoria, preco, disponivel=True):
        produto = Produto(
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            preco=preco,
            disponivel=disponivel,
        )
        self.produtos_repository.cadastrar_produto(produto)
