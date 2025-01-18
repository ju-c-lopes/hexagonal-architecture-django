from enum import Enum


class Categoria(Enum):
    LANCHE = "Lanches"
    ACOMPANHAMENTO = "Acompanhamentos"
    BEBIDA = "Bebidas"
    SOBREMESA = "Sobremesas"


class Produto:
    def __init__(
        self,
        id,
        nome: str,
        descricao: str,
        categoria: Categoria = None,
        preco: float = 0.0,
        disponivel: bool = True,
    ):
        if preco < 0:
            raise ValueError("Preço do produto não pode ser negativo!")
        self._id = id
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.preco = preco
        self.disponivel = disponivel

    def __repr__(self):
        return f"""
{self.categoria}:
    {self.nome}
    Preço = R$ {self.preco:.2f}
"""
