from core.repositories.produtos_repo import ProdutosRepository

class ExcluirProdutoUseCase:
    def __init__(self, produtos_repository: ProdutosRepository):
        self.produtos_repository = produtos_repository

    def execute(self, produto_id):
        if not produto_id:
            raise ValueError("O ID do produto não pode ser vazio.")
        
        deleted_count = self.produtos_repository.excluir_produto_por_id(produto_id)
        
        if deleted_count == 0:
            raise ValueError("Produto não encontrado ou já excluído.")
        
        return deleted_count