import pytest

from src.app import calculate_discount, calculate_tax, calculate_total


@pytest.mark.parametrize(("percent", "expected"), [(0, 80), (25, 60), (100, 0)])
def test_discount(percent, expected):
    assert calculate_discount(80, percent) == expected


@pytest.mark.parametrize(("price", "percent"), [(-1, 10), (80, -1), (80, 101)])
def test_invalid_discount(price, percent):
    with pytest.raises(ValueError):
        calculate_discount(price, percent)


@pytest.mark.parametrize(("prices", "rate", "expected"), [([10, 20], 0.2, 36),
                                                          ([9.99], 0.05, 10.49),
                                                          ([], 0.2, 0)])
def test_total(prices, rate, expected):
    assert calculate_total(prices, rate) == expected


def test_default_tax():
    assert calculate_tax(12) == 2.4


def test_stock_repository(repository):
    assert repository.update_stock("MUG", 5)
    assert repository.get_product("MUG").stock == 95
    assert not repository.update_stock("MUG", 96)
    assert not repository.update_stock("MUG", -1)
    assert not repository.update_stock("ABSENT", 1)
