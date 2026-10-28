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
        if index > 0:
           index = f"{index}. " 
        print(f"{index}{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Active: {self.active}")


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
