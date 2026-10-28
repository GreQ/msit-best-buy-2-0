

import products


class Store:

    def __init__(self, products: list[products.Product] | None = None) -> None:
        self.products = products if products is not None else []

    #add a product to the store's product list
    def add_product(self, product: products.Product) -> None:
        if not isinstance(product, products.Product):
            print("Invalid product type.")
        elif product in self.products:
            print(f"{product.name} is already in the store's product list.")
        else:
            self.products.append(product)

    #remove a product from the store's product list
    def remove_product(self, product: products.Product) -> None:
        if product in self.products:
            self.products.remove(product)
        else:
            print(f"Product {product.name} not found in the store.")

    #get the total quantity of all products in the store
    def get_total_quantity(self) -> int:
        return sum(product.get_quantity() for product in self.products)

    #get a list of all products in the store
    def get_all_products(self) -> list[products.Product]:
        return self.products
    
    #get a list of all available products (products deactivate themselves when out of stock)
    def get_available_products(self) -> list[products.Product]:
        return [product for product in self.products if product.is_active()]

    #print index of all available products with price and quantity
    def show_products(self) -> list[products.Product]:
        available_products = self.get_available_products()
        print ("\n-----\nProducts:")
        for i in range(len(available_products)):
            available_products[i].show(i+1)
        print ("-----")
        #return list in order to pick from by index
        return available_products

    def order(self, cart: list[tuple[products.Product, int]]) -> float:
        total_cost: float = 0
        failures: list[tuple[products.Product, int]] = []
        #join same products in cart, so stock and order limits are checked against the total quantity (no partial orders of same product)
        merged_cart: dict[products.Product, int] = {}
        for product, quantity in cart:
            merged_cart[product] = merged_cart.get(product, 0) + quantity
        for product, quantity in merged_cart.items():
            if product in self.products:
                try:
                    total_cost += product.buy(quantity)
                except ValueError as error:
                    print(error)
                    failures.append((product, quantity))
            else:
                print(f"{product.name} not found in the store.")
        #check if there were any failures and print them
        if failures:
            print("The following items could not be purchased due to insufficient stock or unavailability:")    
            for product, quantity in failures:
                print(f" - {product.name}, quantity:{quantity} (available: {product.is_active()}: quantity: {product.get_quantity()})")
            print ("Please correct order if possible and submit again.")

        return total_cost