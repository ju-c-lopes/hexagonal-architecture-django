class Item:
    def __init__(self, id: int, nome: str, preco: float):
        self.id = id
        self.nome = nome
        self.preco = preco

    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome}, preço=R$ {self.preco})"
