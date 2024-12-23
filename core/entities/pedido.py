from typing import List


class Item:
    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco


class Pedido:
    def __init__(self, cliente: str, itens: List[Item]):
        self.cliente = cliente
        self.itens = itens

    def calcular_total(self):
        if not len(self.itens):
            raise ValueError("Não é possível criar um pedido sem itens!")
        return sum(item.preco for item in self.itens)