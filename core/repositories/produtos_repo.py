from abc import ABC, abstractmethod

from core.entities.produto import Produto


class ProdutosRepository(ABC):
    @abstractmethod
    def cadastrar_produto(self, produto: Produto):
        pass

    @abstractmethod
    def listar_todos(self):
        pass

    @abstractmethod
    def listar_por_categoria(self, categoria):
        pass

    @abstractmethod
    def excluir_produto_por_id(self, produto_id):
        pass

    @abstractmethod
    def atualizar_produto(self, produto_id, produto_atualizado):
        pass
        
