class Product:
    total_products = 0

    def __init__(self, name, price, quantity=1):
        self.active = True
        self.name = name
        self.price = price
        self.quantity = quantity
        Product.total_products += quantity

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            print("Quantity cannot be negative.")
        else:
            Product.total_products += (quantity - self.quantity)
            self.quantity = quantity

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
            print("Quantity must be greater than zero.")
            return 0
        if self.quantity >= quantity:
            self.quantity -= quantity
            print(f"Bought {quantity} of {self.name}. Remaining stock: {self.quantity}.")
            return quantity * self.price
        else:
            print(f"Not enough stock for {self.name}. Available: {self.quantity}.")
            return 0