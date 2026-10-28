from promotions import Promotion


class Product:
    total_products: int = 0

    def __init__(self, name: str, price: float, quantity: int = 1) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.active = True
        self.name = name
        self.price = price
        self.quantity = quantity
        self.promotions: list[Promotion] = []
        Product.total_products += quantity

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        Product.total_products += (quantity - self.quantity)
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    #first promotion of the product, None if there is none
    def get_promotion(self) -> Promotion | None:
        return self.promotions[0] if self.promotions else None

    #replace all promotions with a single one, None removes all promotions
    def set_promotion(self, promotion: Promotion | None) -> None:
        self.promotions = [promotion] if promotion is not None else []

    def get_promotions(self) -> list[Promotion]:
        return list(self.promotions)

    def add_promotion(self, promotion: Promotion) -> None:
        if promotion not in self.promotions:
            self.promotions.append(promotion)

    def remove_promotion(self, promotion: Promotion) -> None:
        if promotion not in self.promotions:
            raise ValueError(f"{promotion.name} is not a promotion of {self.name}.")
        self.promotions.remove(promotion)

    #total price for quantity, promotions don't stack: the cheapest price for the customer is used
    def get_price(self, quantity: int) -> float:
        prices = [promotion.apply_promotion(self, quantity) for promotion in self.promotions]
        return min([self.price * quantity, *prices])

    #text appended to show() output, empty if no promotion
    def promotion_info(self) -> str:
        if not self.promotions:
            return ""
        label = "Promotion" if len(self.promotions) == 1 else "Promotions (best price applies)"
        return f", {label}: {', '.join(promotion.name for promotion in self.promotions)}"

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def available(self, quantity: int) -> bool:
        if self.quantity <= 0:
            print(f"{self.name} out of stock.")
            return False
        if self.quantity < quantity:
            print(f"Not enough {self.name} in stock. Only {self.quantity} available.")
            return False
        elif not self.is_active():
            print(f"Product {self.name} unavailable.")
            return False
        else:
            return True

    def show(self, index: int = 0) -> None:
        prefix = f"{index}. " if index > 0 else ""
        print(f"{prefix}{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Active: {self.active}{self.promotion_info()}")


    def buy(self, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.is_active():
            raise ValueError(f"Product {self.name} is not active.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock for {self.name}. Available: {self.quantity}.")
        self.quantity -= quantity
        if self.quantity == 0:
            self.deactivate()
        print(f"Bought {quantity} of {self.name}. Remaining stock: {self.quantity}.")
        return self.get_price(quantity)


#product without physical stock (e.g. a software license), quantity always stays 0
class NonStockedProduct(Product):

    def __init__(self, name: str, price: float) -> None:
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int) -> None:
        if quantity != 0:
            raise ValueError(f"{self.name} is not stocked, quantity must stay 0.")

    def available(self, quantity: int) -> bool:
        if not self.is_active():
            print(f"Product {self.name} unavailable.")
            return False
        return True

    def show(self, index: int = 0) -> None:
        prefix = f"{index}. " if index > 0 else ""
        print(f"{prefix}{self.name}, Price: ${self.price}, Quantity: Unlimited (non-stocked), Active: {self.active}{self.promotion_info()}")

    def buy(self, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.is_active():
            raise ValueError(f"Product {self.name} is not active.")
        print(f"Bought {quantity} of {self.name}.")
        return self.get_price(quantity)


#product that can only be purchased up to a maximum quantity per order (e.g. shipping fee)
class LimitedProduct(Product):

    def __init__(self, name: str, price: float, quantity: int, maximum: int) -> None:
        super().__init__(name, price, quantity)
        if maximum < 1:
            raise ValueError("Maximum must be at least 1.")
        self.maximum = maximum

    def available(self, quantity: int) -> bool:
        if quantity > self.maximum:
            print(f"{self.name} is limited to {self.maximum} per order.")
            return False
        return super().available(quantity)

    def show(self, index: int = 0) -> None:
        prefix = f"{index}. " if index > 0 else ""
        print(f"{prefix}{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Limited to {self.maximum} per order!, Active: {self.active}{self.promotion_info()}")

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"{self.name} is limited to {self.maximum} per order.")
        return super().buy(quantity)
