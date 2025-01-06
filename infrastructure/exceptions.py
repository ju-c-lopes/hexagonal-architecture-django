class DocumentNotFoundError(Exception):
    """Exceção para quando um documento não é encontrado no repositório."""
    def __init__(self, mensagem="Documento não encontrado"):
        self.mensagem = mensagem
        super().__init__(self.mensagem)
