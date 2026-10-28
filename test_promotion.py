import pytest

from products import LimitedProduct, NonStockedProduct, Product
from promotions import PercentDiscount, Promotion, SecondHalfPrice, ThirdOneFree


def test_promotion_is_abstract() -> None:
    with pytest.raises(TypeError):
        Promotion("General promotion")  # type: ignore[abstract]


def test_percent_discount() -> None:
    product = Product("Google Pixel 7", price=500, quantity=250)
    promotion = PercentDiscount("30% off!", percent=30)
    assert promotion.apply_promotion(product, 2) == 700


def test_percent_discount_with_invalid_percent_raises() -> None:
    with pytest.raises(ValueError):
        PercentDiscount("Too much", percent=120)


def test_second_half_price() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    promotion = SecondHalfPrice("Second Half price!")
    assert promotion.apply_promotion(product, 1) == 1450
    assert promotion.apply_promotion(product, 2) == 2175
    assert promotion.apply_promotion(product, 3) == 3625


def test_third_one_free() -> None:
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    promotion = ThirdOneFree("Third One Free!")
    assert promotion.apply_promotion(product, 2) == 500
    assert promotion.apply_promotion(product, 3) == 500
    assert promotion.apply_promotion(product, 7) == 1250


def test_set_and_get_promotion() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.promotion is None
    promotion = SecondHalfPrice("Second Half price!")
    product.promotion = promotion
    assert product.promotion is promotion


def test_set_promotion_none_removes_promotion() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.promotion = SecondHalfPrice("Second Half price!")
    product.promotion = None
    assert product.promotion is None
    assert product.buy(2) == 2900


def test_buy_applies_promotion() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.promotion = SecondHalfPrice("Second Half price!")
    assert product.buy(2) == 2175
    assert product.quantity == 98


def test_buy_applies_promotion_on_non_stocked_product() -> None:
    product = NonStockedProduct("Windows License", price=125)
    product.promotion = PercentDiscount("30% off!", percent=30)
    assert product.buy(2) == 175


def test_buy_applies_promotion_on_limited_product() -> None:
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    product.promotion = PercentDiscount("50% off!", percent=50)
    assert product.buy(1) == 5


def test_same_promotion_on_multiple_products() -> None:
    promotion = PercentDiscount("10% off!", percent=10)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    mac.promotion = promotion
    pixel.promotion = promotion
    assert mac.buy(1) == 1305
    assert pixel.buy(1) == 450


def test_show_includes_promotion(capsys: pytest.CaptureFixture[str]) -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.promotion = SecondHalfPrice("Second Half price!")
    print(product)
    assert "Promotion: Second Half price!" in capsys.readouterr().out


def test_add_multiple_promotions() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    product.add_promotion(second_half_price)
    product.add_promotion(third_one_free)
    product.add_promotion(second_half_price)
    assert product.promotions == [second_half_price, third_one_free]


def test_multiple_promotions_use_best_price() -> None:
    product = Product("Bose QuietComfort Earbuds", price=100, quantity=500)
    product.add_promotion(SecondHalfPrice("Second Half price!"))
    product.add_promotion(ThirdOneFree("Third One Free!"))
    # 2 items: second half price 150 < third one free 200
    assert product.get_price(2) == 150
    # 3 items: third one free 200 < second half price 250
    assert product.get_price(3) == 200


def test_remove_promotion() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    product.add_promotion(second_half_price)
    product.add_promotion(third_one_free)
    product.remove_promotion(second_half_price)
    assert product.promotions == [third_one_free]


def test_remove_missing_promotion_raises() -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    with pytest.raises(ValueError):
        product.remove_promotion(ThirdOneFree("Third One Free!"))


def test_show_lists_multiple_promotions(capsys: pytest.CaptureFixture[str]) -> None:
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.add_promotion(SecondHalfPrice("Second Half price!"))
    product.add_promotion(ThirdOneFree("Third One Free!"))
    print(product)
    output = capsys.readouterr().out
    assert "Second Half price!" in output
    assert "Third One Free!" in output
