import pytest

from products import LimitedProduct, NonStockedProduct, Product


def test_create_normal_product() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.active


def test_create_product_with_empty_name_raises() -> None:
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_with_negative_price_raises() -> None:
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero_quantity() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=2)
    product.buy(2)
    assert product.quantity == 0
    assert not product.active


def test_buy_modifies_quantity_and_returns_total_price() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    total_price = product.buy(3)
    assert total_price == 4350
    assert product.quantity == 97


def test_buy_more_than_in_stock_raises() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.buy(6)


def test_set_negative_price_raises() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    with pytest.raises(ValueError):
        product.price = -100
    assert product.price == 1450


def test_set_quantity_to_zero_deactivates_product() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.quantity = 0
    assert not product.active


def test_set_negative_quantity_raises() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    with pytest.raises(ValueError):
        product.quantity = -1


def test_non_stocked_product_quantity_stays_zero() -> None:
    product = NonStockedProduct("Windows License", price=125)
    assert product.quantity == 0
    with pytest.raises(ValueError):
        product.quantity = 5


def test_str() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert str(product) == "MacBook Air M2, Price: $1450, Quantity: 100"


def test_str_of_special_products() -> None:
    assert "Unlimited" in str(NonStockedProduct("Windows License", price=125))
    assert "Limited to 1 per order" in str(LimitedProduct("Shipping", price=10, quantity=250, maximum=1))


def test_compare_prices() -> None:
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert mac > bose
    assert bose < mac
    assert not mac < bose


def test_products_with_same_price_are_not_equal() -> None:
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    other = Product("Other Phone", price=500, quantity=10)
    assert pixel != other
    assert not pixel > other
    assert not pixel < other
