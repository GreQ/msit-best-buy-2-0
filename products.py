from promotions import Promotion


class Product:
    total_products: int = 0

    def __init__(self, name: str, price: float, quantity: int = 1) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        #name and price are validated by their property setters
        self.name = name
        self.price = price
        self._quantity = quantity
        self._active = True
        self._promotions: list[Promotion] = []
        Product.total_products += quantity

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        self._name = name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self._price = price

    @property
    def quantity(self) -> int:
        return self._quantity

    #setting quantity to 0 deactivates the product
    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        Product.total_products += (quantity - self._quantity)
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        self._active = active

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    #first promotion of the product, None if there is none
    @property
    def promotion(self) -> Promotion | None:
        return self._promotions[0] if self._promotions else None

    #replace all promotions with a single one, None removes all promotions
    @promotion.setter
    def promotion(self, promotion: Promotion | None) -> None:
        self._promotions = [promotion] if promotion is not None else []

    #copy of all promotions, use add_promotion/remove_promotion to change them
    @property
    def promotions(self) -> list[Promotion]:
        return list(self._promotions)

    def add_promotion(self, promotion: Promotion) -> None:
        if promotion not in self._promotions:
            self._promotions.append(promotion)

    def remove_promotion(self, promotion: Promotion) -> None:
        if promotion not in self._promotions:
            raise ValueError(f"{promotion.name} is not a promotion of {self.name}.")
        self._promotions.remove(promotion)

    #total price for quantity, promotions don't stack: the cheapest price for the customer is used
    def get_price(self, quantity: int) -> float:
        prices = [promotion.apply_promotion(self, quantity) for promotion in self._promotions]
        return min([self.price * quantity, *prices])

    #text appended to __str__ output, empty if no promotion
    def _promotion_info(self) -> str:
        if not self._promotions:
            return ""
        label = "Promotion" if len(self._promotions) == 1 else "Promotions (best price applies)"
        return f", {label}: {', '.join(promotion.name for promotion in self._promotions)}"

    def __str__(self) -> str:
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}{self._promotion_info()}"

    #compare products by price, no __eq__ so products stay unique by identity (needed for `in` and cart merging)
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def available(self, quantity: int) -> bool:
        if self.quantity <= 0:
            print(f"{self.name} out of stock.")
            return False
        if self.quantity < quantity:
            print(f"Not enough {self.name} in stock. Only {self.quantity} available.")
            return False
        elif not self.active:
            print(f"Product {self.name} unavailable.")
            return False
        else:
            return True

    def buy(self, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.active:
            raise ValueError(f"Product {self.name} is not active.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock for {self.name}. Available: {self.quantity}.")
        self.quantity -= quantity
        print(f"Bought {quantity} of {self.name}. Remaining stock: {self.quantity}.")
        return self.get_price(quantity)


#product without physical stock (e.g. a software license), quantity always stays 0
class NonStockedProduct(Product):

    def __init__(self, name: str, price: float) -> None:
        super().__init__(name, price, quantity=0)

    @property
    def quantity(self) -> int:
        return 0

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if quantity != 0:
            raise ValueError(f"{self.name} is not stocked, quantity must stay 0.")

    def available(self, quantity: int) -> bool:
        if not self.active:
            print(f"Product {self.name} unavailable.")
            return False
        return True

    def __str__(self) -> str:
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited (non-stocked){self._promotion_info()}"

    def buy(self, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.active:
            raise ValueError(f"Product {self.name} is not active.")
        print(f"Bought {quantity} of {self.name}.")
        return self.get_price(quantity)


#product that can only be purchased up to a maximum quantity per order (e.g. shipping fee)
class LimitedProduct(Product):

    def __init__(self, name: str, price: float, quantity: int, maximum: int) -> None:
        super().__init__(name, price, quantity)
        self.maximum = maximum

    @property
    def maximum(self) -> int:
        return self._maximum

    @maximum.setter
    def maximum(self, maximum: int) -> None:
        if maximum < 1:
            raise ValueError("Maximum must be at least 1.")
        self._maximum = maximum

    def available(self, quantity: int) -> bool:
        if quantity > self.maximum:
            print(f"{self.name} is limited to {self.maximum} per order.")
            return False
        return super().available(quantity)

    def __str__(self) -> str:
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Limited to {self.maximum} per order!{self._promotion_info()}"

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"{self.name} is limited to {self.maximum} per order.")
        return super().buy(quantity)
