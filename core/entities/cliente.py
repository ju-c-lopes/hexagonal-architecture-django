from bson import ObjectId


class Cliente:
    """Entidade Cliente."""

    def __init__(self, nome: str, email: str, cpf: str, id: ObjectId = None) -> None:
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def __repr__(self):
        return f"Cliente(nome={self.nome}, email={self.email}, cpf={self.cpf})"
