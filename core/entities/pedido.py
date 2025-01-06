from typing import List

from core.entities.cliente import Cliente
from core.entities.item import Item


class Pedido:
    def __init__(self, id, cliente: Cliente, itens: List[Item], status: str):
        if not isinstance(cliente, Cliente):
            raise ValueError("O cliente deve ser uma instância de Cliente.")
        self.id = id
        self.cliente = cliente
        self.itens = itens
        self.status = status

    def __repr__(self):
        return f"Pedido(id={self.id}, cliente={self.cliente}, itens={[item for item in self.itens]}, status={self.status})"

    def calcular_total(self):
        if not len(self.itens):
            raise ValueError("Não é possível criar um pedido sem itens!")
        return sum(item.preco for item in self.itens)
