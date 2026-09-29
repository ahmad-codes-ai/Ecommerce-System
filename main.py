import models
import services
import auth
import analytics



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
            print("4: See cart")
            print("5: Remove item from cart")
            print("6: Checkout")
            print("7: Quit")

        elif isinstance(self.current_user,models.Driver):
            print(f"Hello {self.current_user.name} Welcome to Driver dashboard")
            print("1: See and pick orders")
            print("2: Show completed orders")
            print("3: Show active orders")
            print("4: Show earnings")
            print("5: Deliver Order")
            print("6: Quit")

        elif self.current_user == 'admin':
            print(f"-------------- Welcome to Admin Dashboard ---------------")
            print(f"Your current Balance is: {services.get_admin_balance()}$")
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
                self.handle_show_cart()
            elif choice == 5:
                self.handle_remove_item_from_cart()
            elif choice == 6:
                self.handle_checkout()
            elif choice == 7:
                self.handle_exit()


        elif isinstance(self.current_user,models.Driver):
            if choice == 1:
                self.handle_show_orders_driver()
            elif choice == 2:
                self.show_completed_orders()
            elif choice == 3:
                self.handle_show_active_orders()
            elif choice == 4:
                self.show_earnings()
            elif choice == 5:
                self.handle_deliver_order()
            elif choice == 6:
                self.handle_exit()

        elif self.current_user == 'admin':
            if choice == 1:
                self.handle_show_all_products()
            elif choice == 2:
                self.handle_add_product()
            elif choice == 3:
                self.handle_restock_product()
            elif choice == 4:
                self.handle_low_stock_products()
            elif choice == 5:
                self.handle_analytics_dashboard()
            elif choice == 6:
                self.handle_exit()

    def handle_signup(self):
        role = input("For User type (u) for Driver type (d): ")
        if role == 'u':
            role = 'user'
        elif role == 'd':
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
        role = input("If your are a user enter (u) and for driver (d): ")

        if role == 'u':
            actor = 'user'
        elif role == 'd':
            actor = 'driver'
        else:
            actor = None
    
        email = input("Enter your email: ")
        password = input("Enter your password: ")
      
        result = auth.login(email,password,actor)
        if result is not False and result is not None:
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


    def handle_show_cart(self):
        if len(self.current_user.cart) > 0:
            print(f"Your cart: {self.current_user.cart}")
        else:
            print("Your cart is empty []")


    def handle_remove_item_from_cart(self):
        if len(self.current_user.cart) > 0:
            print("-------------- Your Cart ----------------")
            print(self.current_user.cart)

            id = input("Enter the id of which product you wanna remove: ")
            self.current_user.remove_item_from_cart(id)
        else:
            print("Your cart is empty nothing to remove")


    def handle_show_order_status(self):
        services.show_all_orders(self.current_user)

        user = input("Enter id of any order to see details or enter (q) for exit: ")

        if user == 'q':
            return 
        else:
            print(services.show_order_details(user))


    def handle_show_all_products(self):
        services.show_products()


    def handle_add_product(self):
        name = input("Enter name of the product: ")
        cp = int(input("Enter cost price of the product: "))
        sp = int(input("Enter selling price of the product: "))
        quan = int(input("Enter quantity: "))

        result = services.add_product(name,cp,sp,quan)

        if result:
            print("Product created successfully")
        else:
            print(f"Your balance {services.get_admin_balance()} is not enough to create this product")


    def handle_restock_product(self):
        id = int(input("Enter the id of the product: "))
        quan = int(input("Enter quantity to add: "))

        result = services.restock_product(id,quan)

        if result is True:
            print("The product stock has increased")
        elif result is False:
            print(f"Your balance {services.get_admin_balance()} is not enough to restock the quantity given")
        else:
            print("No product found with this id")


    def handle_low_stock_products(self):
        result = analytics.get_low_stock_products()

        print("Product with these id's has stock < 5")
        print(result)


    def handle_analytics_dashboard(self):
        print("1: Show financial Analytics")
        print("2: Show Orders Analytics")
        print("3: Show Products Analytics")
        print("4: Show all transaction logs")

        user = int(input("Enter your choice: "))

        if user == 1:
            print(f"Total Spent: \t \t {analytics.show_total_spent()} ")
            print(f"Total Revenu: \t \t {analytics.show_total_revenu()}")
            print(f"Total Profit: \t \t {analytics.show_total_profits()}")

        elif user == 2:
            print(f"Total Orders: \t \t {analytics.get_total_orders()}")
            print(f"Pending Orders: \t \t {analytics.get_pending_orders()}")
            print(f"Assigned Orders: \t \t {analytics.get_assigned_orders()}")
            print(f"Delivered Orders: \t \t {analytics.get_delivered_orders()}")

        elif user == 3:
            print(f"Total Number of Products: \t \t {analytics.total_number_of_products()}")
            print(f"Total Inventory value: \t \t {analytics.get_total_inventory_value()}")
            print(f"Low stock Products < 5: \t \t {analytics.get_low_stock_products()}")
            print(f"Out of Stock Products: \t \t {analytics.get_out_of_stock_products()}")
            print(f"Top sold product: \t \t {analytics.most_sold_product()}")
            print(f"Top 3 products: \t \t {analytics.get_top_sold_products(3)}")

        elif user == 4:
            print("All Tranactions Logs: ")
            print(analytics.show_all_logs())

        else:
            print("Invalid Input")

# Driver Handlers

    def handle_show_orders_driver(self):
        city_orders = services.get_orders_by_city(self.current_user.location)  # All orders pending,assigned,delivered

        if len(city_orders) > 0:
            i = 1
            for order in city_orders:

                if services.get_order_status(order) == 'pending':
                    print(order,end=' ')
                    services.show_order(order)
                    i+=1
                    print()

            user = input("Enter the ids of order you wanna pick in order id1,id2,id3: ")
            requested_ids = user.split(',')

            for id in requested_ids:
                if services.get_driver_active_orders_count(self.current_user.id) <= 20:
                    services.assign_driver_order(id,self.current_user.id)
                else:
                    print("Your 20 orders limit reached some orders are not assigned to you")
            
        else:
            print("No Order from your city right now")
     
    # Function is working and updating order driver and status
    

    def handle_show_active_orders(self):
        result = services.get_driver_active_orders_details(self.current_user.id)

        for id,total in result:
            print((id,total))


    def handle_deliver_order(self):
        
        self.handle_show_active_orders()
        active_orders = services.get_driver_active_orders_details(self.current_user.id)

        user = input("Enter the id of which order you have delivered or 'a' for all: ")

        if user == 'a':
            for id,total in active_orders:
                services.complete_delivery(id)
            print(f"You have delivered all your orders. Your new balance is: {services.get_driver_earning(self.current_user.id)}")

        else:
            services.complete_delivery(user)
            print(f"The order is delivered. Your new balance is: {services.get_driver_earning(self.current_user.id)}")


    def show_completed_orders(self):
        print("Your completed orders are: ")
        for order in services.get_completed_orders_rider(self.current_user.id):
            print(order)

    


    # Now just need to implement driver balance logic. Need to be saved in file 
    # The balamce of driver is still increasing if he enter any random order id need to check this 



app = App()
app.run()



# Testing 1 results:

# Stock is not reduced in products.json when adding to cart 
# Finance is not updated 
# Add see cart and remove item from cart in handlers


# Testing 2 results:

# All issues of test 1 has been resolved
# carts.json has no usecase
# the output need to be formatted proper spacing from the print commands 
# Order status need to implemented in handlers
# one more option to see current orders



# Testing 3 results (Admin):

# Products ids are not 




