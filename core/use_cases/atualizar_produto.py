from core.repositories.produtos_repo import ProdutosRepository

class AtualizarProdutoUseCase:
    def __init__(self, produtos_repository: ProdutosRepository):
        self.produtos_repository = produtos_repository

    def execute(self, produto_id, produto_atualizado: dict):
        if not produto_id:
            raise ValueError("O ID do produto não pode ser vazio.")
        
        if not produto_atualizado:
            raise ValueError("Os dados atualizados do produto não podem ser vazios.")
        
        modified_count = self.produtos_repository.atualizar_produto(produto_id, produto_atualizado)
        
        if modified_count == 0:
            raise ValueError("Produto não encontrado ou não atualizado.")
        
        return modified_count