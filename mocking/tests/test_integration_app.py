import pytest


def test_purchase(service, repository):
    assert service.place_order("MUG", 2) == {
        "success": True, "item": "Coffee Mug", "quantity": 2, "total": 28.8,
    }
    assert repository.get_product("MUG").stock == 98


@pytest.mark.parametrize(("sku", "quantity", "error"), [
    ("ABSENT", 1, "Product not found"),
    ("SHIRT", 51, "Not enough stock"),
    ("SHIRT", 0, "Quantity must be a positive integer"),
    ("SHIRT", 1.5, "Quantity must be a positive integer"),
])
def test_rejected_purchase(service, repository, sku, quantity, error):
    assert service.place_order(sku, quantity) == {"success": False, "error": error}
    assert repository.get_product("SHIRT").stock == 50


@pytest.mark.slow
def test_order_batch_until_stock_is_depleted(service, repository):
    for _ in range(30):
        assert service.place_order("HAT", 1)["success"]
    assert repository.get_product("HAT").stock == 0
    assert not service.place_order("HAT", 1)["success"]
