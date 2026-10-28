

import products


class Store:

    def __init__(self, products=None):
        self.products = products if products is not None else []

    #add a product to the store's product list
    def add_product(self, product):
        if type(product) is not products.Product:
            print("Invalid product type.")
        elif product in self.products:
            print(f"{product.name} is already in the store's product list.")
        else:
            self.products.append(product)

    #remove a product from the store's product list
    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)
        else:
            print(f"Product {product.name} not found in the store.")

    #get the total quantity of all products in the store
    def get_total_quantity(self):
        return sum(product.get_quantity() for product in self.products)

    #get a list of all products in the store
    def get_all_products(self):
        return self.products
    
    #get a list of all available (active + in stock) products
    def get_available_products(self):
        return [product for product in self.products if product.is_active() and product.get_quantity() > 0]

    #print index of all available products with price and quantity
    def show_products(self):
        available_products = self.get_available_products()
        print ("\n-----\nProducts:")
        for i in range(len(available_products)):
            available_products[i].show(i+1)
        print ("-----")
        #return list in order to pick from by index
        return available_products

    def order(self, cart):
        total_cost = 0
        failures = [];
        #todo: join same products/quantity in cart in order to failure if not enough stock and place no partial orders of same product. 
        for product, quantity in cart:
            if product in self.products:
                price_product = product.buy(quantity)
                if price_product:
                    total_cost += price_product
                else:
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