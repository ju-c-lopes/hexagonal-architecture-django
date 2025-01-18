from typing import List

from core.entities import TipoCadastro
from core.entities.cliente import Cliente
from core.entities.produto import Produto


class Pedido:
    def __init__(
        self,
        cliente: Cliente,
        produtos: List[Produto],
        personalizacao: str = None,
        cadastro: str = None,
        codigo_do_pedido: str = None,
        status: str = "PENDENTE",
        total: float = 0.0,
    ):
        self.cliente = cliente
        self.produtos = produtos
        self.personalizacao = personalizacao
        self.cadastro = self.set_cadastro()
        self.codigo_do_pedido = codigo_do_pedido
        self.status = status
        self.total = self.calcular_total()

    def __repr__(self):
        return f"""
Pedido(cliente={self.cliente}
produtos={[produto for produto in self.produtos]}
OBSERVAÇÃO: {self.personalizacao}
COD: {self.codigo_do_pedido}
Total: R$ {self.total:.2f}
status={self.status})
"""

    def set_cadastro(self):
        return TipoCadastro[1][0] if self.cliente else TipoCadastro[0][0]

    def calcular_total(self):
        if not len(self.produtos) or len(self.produtos) == 0:
            raise ValueError("Não é possível criar um pedido sem produtos!")
        try:
            return sum(produto.preco for produto in self.produtos)
        except Exception:
            pass
