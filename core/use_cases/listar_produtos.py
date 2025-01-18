from core.entities.pedido import Pedido
from core.entities.produto import Categoria
from core.repositories.produtos_repo import ProdutosRepository


class ListarProdutosUseCase:
    def __init__(self, produtos_repository: ProdutosRepository):
        self.produtos_repository = produtos_repository
        self.listar_itens_por_categoria = ListarItensPorCategoriaUseCase(
            produtos_repository=self.produtos_repository
        )
        self.produtos = self.produtos_repository.listar_todos()

    def execute(self, produtos_do_pedido=[], personalizacao=None):
        menu = []
        for categoria in Categoria:
            # Listar itens da categoria atual
            produtos = self.listar_itens_por_categoria.execute(categoria, self.produtos)
            menu.append(self.selecionar_produtos(categoria, produtos))

        return [
            (produto[0].categoria, produto[1])
            for produto_menu in menu
            for produto in produto_menu
        ]

    def selecionar_produtos(self, categoria, produtos):
        """
        Este método seria substituído por uma interação real no frontend,
        mas aqui simulamos a escolha do cliente.
        """
        menu = []
        numero_do_produto = 1
        for produto in produtos:
            msg = f"{numero_do_produto}- {produto.nome} - R$ {produto.preco:.2f}"
            menu.append((produto, msg))
            numero_do_produto += 1

        # escolha = input("Escolha um número ou pressione Enter para pular: ")
        # return produtos[int(escolha) - 1] if escolha else None
        return menu

    def montar_pedido(self, dados_do_pedido, cliente):
        menu = []
        for categoria in Categoria:
            produtos = self.listar_itens_por_categoria.execute(categoria, self.produtos)
            menu.append(self.selecionar_produtos(categoria, produtos))

        produtos_do_pedido = []

        for dado, entrada_do_cliente in dados_do_pedido.items():
            if entrada_do_cliente is not None and dado == "Personalizacao":
                personalizacao = entrada_do_cliente
            elif entrada_do_cliente is not None:
                try:
                    entrada_do_cliente = int(entrada_do_cliente)
                except Exception:
                    entrada_do_cliente = None

                for categoria in menu:
                    # Se a entrada do cliente for None, pulará para a próxima categoria
                    if entrada_do_cliente is None:
                        continue

                    if dado == categoria[0][0].categoria:
                        produtos_do_pedido.append(categoria[entrada_do_cliente - 1][0])
        if len(produtos_do_pedido) < 1:
            return None

        pedido = Pedido(
            cliente=cliente,
            produtos=produtos_do_pedido,
            personalizacao=personalizacao,
        )

        return pedido


class ListarItensPorCategoriaUseCase:
    def __init__(self, produtos_repository: ProdutosRepository):
        self.produtos_repository = produtos_repository

    def execute(self, categoria: Categoria, produtos):
        if not isinstance(categoria, Categoria):
            raise ValueError(f"Categoria inválida: {categoria}")

        produtos_filtrados = [
            produto for produto in produtos if produto.categoria == categoria.name
        ]
        return produtos_filtrados
