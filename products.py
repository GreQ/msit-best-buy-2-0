class Product:
    total_products = 0

    def __init__(self, name, price, quantity=1):
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
        Product.total_products += quantity

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        Product.total_products += (quantity - self.quantity)
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def available(self, quantity) -> bool:
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

    def show(self, index=0):
        prefix = f"{index}. " if index > 0 else ""
        print(f"{prefix}{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Active: {self.active}")


    def buy(self, quantity):
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
        return quantity * self.price


#product without physical stock (e.g. a software license), quantity always stays 0
class NonStockedProduct(Product):

    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity):
        if quantity != 0:
            raise ValueError(f"{self.name} is not stocked, quantity must stay 0.")

    def available(self, quantity) -> bool:
        if not self.is_active():
            print(f"Product {self.name} unavailable.")
            return False
        return True

    def show(self, index=0):
        prefix = f"{index}. " if index > 0 else ""
        print(f"{prefix}{self.name}, Price: ${self.price}, Quantity: Unlimited (non-stocked), Active: {self.active}")

    def buy(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.is_active():
            raise ValueError(f"Product {self.name} is not active.")
        print(f"Bought {quantity} of {self.name}.")
        return quantity * self.price


#product that can only be purchased up to a maximum quantity per order (e.g. shipping fee)
class LimitedProduct(Product):

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        if maximum < 1:
            raise ValueError("Maximum must be at least 1.")
        self.maximum = maximum

    def available(self, quantity) -> bool:
        if quantity > self.maximum:
            print(f"{self.name} is limited to {self.maximum} per order.")
            return False
        return super().available(quantity)

    def show(self, index=0):
        prefix = f"{index}. " if index > 0 else ""
        print(f"{prefix}{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Limited to {self.maximum} per order!, Active: {self.active}")

    def buy(self, quantity):
        if quantity > self.maximum:
            raise ValueError(f"{self.name} is limited to {self.maximum} per order.")
        return super().buy(quantity)
