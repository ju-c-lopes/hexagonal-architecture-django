from core.entities.item import Item


def test_item_initialization():
    item = Item(id=1, nome="Hambúrguer", preco=10.0)

    assert item.id == 1
    assert item.nome == "Hambúrguer"
    assert item.preco == 10.0
