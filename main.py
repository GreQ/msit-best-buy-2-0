import store
import products


# setup initial stock of inventory
product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                products.Product("Google Pixel 7", price=500, quantity=250),
                products.NonStockedProduct("Windows License", price=125),
                products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
               ]
best_buy = store.Store(product_list)
cart = []
active_options = "main_options"

def show_main_options(shop):
    routes = [
        ["List all products in store", shop.show_products],
        ["Show total amount in store",  lambda: print(f"Total products in store: {shop.get_total_quantity()}")],
        ["Make an order", lambda: show_order_options(shop)],
        ["Quit", lambda: exit()]
    ];
    active_options = "main_options"
    while active_options == "main_options":
        print("\n***** Store Menu *****")
        for i, route in enumerate(routes):
            print(f"{i + 1}. {route[0]}")
        choice = input("Enter your choice (1-4): ")
        if choice.isdigit() and 1 <= int(choice) <= len(routes):
            routes[int(choice) - 1][1]()
        else:
            print("Invalid choice. Please try again.")

def show_order_options(shop):
    active_options = "order_options"
    while active_options == "order_options":
        print("\nTo finish order just hit return.")
        available_products = shop.show_products()
        #get product index
        input_product = input("Which product # do you want? ")
        if input_product.isdigit() and int(input_product) <= len(available_products):
            product = available_products[int(input_product)-1]
            #get quantity for product
            input_quantity = input(f"How many '{product.name}s' do you want to order? ")
            if input_quantity.isdigit():
                quantity =int(input_quantity)
                if quantity > 0:
                    #stock left after what is already in cart
                    remaining = product.get_quantity() - sum(q for p, q in cart if p == product)
                    if product.get_quantity() > 0 and remaining < quantity:
                        #auto adjust quantity to remaining stock if not enough stock (non-stocked products have quantity 0)
                        if remaining > 0:
                            print(f"Not enough stock for {product.name}. We adjusted your order to the remaining quantity of {remaining}.")
                            add_to_cart(product, remaining)
                        else:
                            print(f"All available {product.name} are already in your cart.")
                    else:
                        add_to_cart(product, quantity)
                else:
                    remove_from_cart(product)
            else:
                print(f"Invalid quantity. Please enter a number  from 1 to {len(available_products)}.")
                show_main_options(shop)
        elif input_product.strip() == "":
            print("Order finished.")
            show_cart()
            confirm = input("Do you want to place the order? (yes/no): ")
            if confirm.lower() == "yes":
                total_cost = shop.order(cart)
                print(f"Order placed successfully! Total cost: ${total_cost}")
            else:
                print("Order canceled.")
            cart.clear()
            show_main_options(shop)
        else:
            print("Invalid choice. Please try again.")

def show_cart():
    if not cart:
        print("Your cart is empty.")
        return
    print("\n-----\nYour cart:")
    price_total = 0
    for i, (product, quantity) in enumerate(cart):
        price_product = product.price * quantity
        price_total += price_product
        print(f"{i + 1}. {product.name} - Quantity: {quantity} - Price: ${price_product}")
    print(f"Total cost: ${price_total}")
    print("-----")

def add_to_cart(product, quantity):
    #merge with quantity of same product already in cart
    in_cart = sum(q for p, q in cart if p == product)
    if product.available(in_cart + quantity):
        cart[:] = [(p, q) for p, q in cart if p != product]
        cart.append((product, in_cart + quantity))
        print(f"Added {quantity} {product.name} to cart.")
        show_cart()
    else:
        print(f"Could not add {quantity} {product.name} to cart.")

def remove_from_cart(product):
    global cart
    cart = [(p, q) for p, q in cart if p != product]
    print(f"Removed {product.name} from cart.")
    show_cart()


def task1(shop):
    products = shop.get_all_products()
    print(shop.get_total_quantity())
    print(shop.order([(products[0], 2), (products[1], 3)]))

def start(shop):
    shop.add_product(products.Product("Banana", 0.35, 5))
    shop.add_product(products.Product("Lemon", 0.8, 15))
    shop.add_product(products.Product("Apple", 0.22, 22))
    show_main_options(shop)

#task1(shop)
start(best_buy)
