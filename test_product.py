import pytest

from products import Product


def test_create_normal_product() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.get_quantity() == 100
    assert product.is_active()


def test_create_product_with_empty_name_raises() -> None:
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_with_negative_price_raises() -> None:
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero_quantity() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=2)
    product.buy(2)
    assert product.get_quantity() == 0
    assert not product.is_active()


def test_buy_modifies_quantity_and_returns_total_price() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    total_price = product.buy(3)
    assert total_price == 4350
    assert product.get_quantity() == 97


def test_buy_more_than_in_stock_raises() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.buy(6)
