from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


#abstract base for all promotions, a promotion can be shared by multiple products
class Promotion(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    #return the total price for quantity of product after promotion was applied
    @abstractmethod
    def apply_promotion(self, product: Product, quantity: int) -> float:
        pass


#percentage off the total price (e.g. 30% off)
class PercentDiscount(Promotion):

    def __init__(self, name: str, percent: float) -> None:
        super().__init__(name)
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100.")
        self.percent = percent

    def apply_promotion(self, product: Product, quantity: int) -> float:
        return product.price * quantity * (100 - self.percent) / 100


#every second item costs half price
class SecondHalfPrice(Promotion):

    def apply_promotion(self, product: Product, quantity: int) -> float:
        half_price_items = quantity // 2
        return product.price * (quantity - half_price_items) + product.price / 2 * half_price_items


#buy 2, get the 3rd one free
class ThirdOneFree(Promotion):

    def apply_promotion(self, product: Product, quantity: int) -> float:
        free_items = quantity // 3
        return product.price * (quantity - free_items)
