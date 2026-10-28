from products import Product
from store import Store


def test_product_in_store() -> None:
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    best_buy = Store([mac, bose])
    assert mac in best_buy
    assert pixel not in best_buy


def test_combine_stores() -> None:
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    store1 = Store([mac, bose])
    store2 = Store([pixel])
    combined = store1 + store2
    assert isinstance(combined, Store)
    assert combined.get_all_products() == [mac, bose, pixel]
    # original stores are unchanged
    assert pixel not in store1
    assert mac not in store2


def test_combine_stores_without_duplicates() -> None:
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    combined = Store([mac, bose]) + Store([mac])
    assert combined.get_all_products() == [mac, bose]
