import models
import services
import auth


class App():
    def __init__(self):
        self.current_user = None
        self.is_running = True

    def show_menu(self):
        if self.current_user is None:
            print("-------------- Welcome to Ecommerce Store ----------------")
            print("1: Signup")
            print("2: Login")
            print("3: Quit")

        elif isinstance(self.current_user,models.User):
            print(f"Hello {self.current_user.name} Welcome to Ecommerce Store")
            print("1: Browse Products")
            print("2: Buy by id")
            print("3: See order status")
            print("4: Checkout")
            print("5: Quit")

        elif isinstance(self.current_user,models.Driver):
            print(f"Hello {self.current_user.name} Welcome to Driver dashboard")
            print("1: See and pick orders")
            print("2: Start Trip")
            print("3: Quit")

        elif isinstance(self.current_user,models.Admin):
            print(f"-------------- Welcome to Admin Dashboard ---------------")
            print(f"Your current Balance is: {self.current_user.balance}")
            print("1: See all products")
            print("2: Add product")
            print("3: Restock Product")
            print("4: Products with low quantity")
            print("5: See Analytics Dashboard")
            print("6: Quit")

        else:
            print("Invalid")

    def run(self):
        while self.is_running:
            self.show_menu()
            choice = int(input("Enter your choice: "))
            self.handle_choice(choice)

    def handle_choice(self,choice):

        if self.current_user is None:
            if choice == 1:
                self.handle_signup()
            elif choice == 2:
                self.handle_login()
            elif choice == 3:
                self.handle_exit()

        elif isinstance(self.current_user,models.User):
            if choice == 1:
                self.handle_browse_products()
            elif choice == 2:
                self.handle_buy_by_id()
            elif choice == 3:
                self.handle_show_order_status()
            elif choice == 4:
                self.handle_checkout()
            elif choice == 5:
                self.handle_exit()


        elif isinstance(self.current_user,models.Driver):
            if choice == 1:
                self.handle_show_orders_driver()
            elif choice == 2:
                self.handle_start_rider_trip()
            elif choice == 3:
                self.handle_exit()

        elif isinstance(self.current_user,models.Admin):
            if choice == 1:
                self.handle_show_all_products()
            elif choice == 2:
                self.handle_add_product()
            elif choice == 3:
                self.handle_restock_product()
            elif choice == 4:
                self.handle_low_quantity_products()
            elif choice == 5:
                self.handle_analytics_dashboard()
            elif choice == 6:
                self.handle_exit()

    def handle_signup(self):
        role = input("For User type (u) for Driver type (d): ")
        if role == 'u':
            role = 'user'
        elif role == 'r':
            role = 'driver'

        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Create a strong password: ")
        location = input("Plz enter your city: ")

        result = auth.sign_up(name,email,password,location,role)

        if result:
            print("Your account has been registered successfully.")
        else:
            print("This email is already associated with an account. Please login")

    def handle_login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        result = auth.login(email,password)

        if result is not False:
            self.current_user = result
            print("Login Successfull")
        else:
            print("Login Failed Plz try again")

    def handle_exit(self):
        print("Thanks For using Bye!")
        self.is_running = False


    def handle_browse_products(self):
        services.show_products()

        id = input("Enter the id of any product you wanna buy or type (n): ")

        if id == 'n':
            return 

        if services.product_exist(id):
            quantity = int(input("Enter the quantity: "))
            result = self.current_user.add_item_to_cart(id,quantity)

            if result:
                print("The item has been added to your cart")
            else:
                print(f"The required quantity is not available for this product. Current stock is: {services.get_product_stock(id)}")

        else:
            print("No product is found with this id")


    def handle_buy_by_id(self):
        id = input("Enter the id of the product: ")

        if services.product_exist(id):
            quan = int(input("Enter the quantity: "))
            result = self.current_user.add_item_to_cart(id,quan)

            if result:
                print("Item Successfully added in cart")
            else:
                print(f"The required quantity is not available for this product. Current stock is: {services.get_product_stock(id)}")

        else:
            print("No product is found with this id")


    def handle_checkout(self):
        result = services.checkout(self.current_user)

        if result:
            print(f"You order has been placed and your cart is now empty. Your order id is: {result} remeber this to track order")
        else:
            print("Your cart is empty plz add an item to cart before checkout")




app = App()


app.run()



# Testing 1 results:

# Stock is not reduced in products.json when adding to cart 
# Finance is not updated 
# Add see cart and remove item from cart in handlers











