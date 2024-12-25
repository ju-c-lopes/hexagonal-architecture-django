class Cliente:
    """Entidade Cliente."""

    def __init__(self, id, nome: str, email: str, cpf: str) -> None:
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
