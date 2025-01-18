from abc import ABC, abstractmethod

from core.entities.cliente import Cliente


class ClienteRepository(ABC):
    """Interface de contrato para repositórios de clientes."""

    @abstractmethod
    def salvar(self, cliente: Cliente) -> None:
        """Salva um cliente no repositório."""
        pass

    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Cliente:
        """Busca um cliente pelo CPF."""
        pass
