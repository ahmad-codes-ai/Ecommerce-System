import models

class Menu():
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
            print("2: Search by id")
            print("3: See order status")
            print("4: Quit")

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
                self.browse_product()
            elif choice == 2:
                self.search_by_id()
            elif choice == 3:
                self.show_order_status()
            elif choice == 4:
                self.handle_exit()

        elif isinstance(self.current_user,models.Driver):
            if choice == 1:
                self.show_orders_driver()
            elif choice == 2:
                self.start_rider_trip()
            elif choice == 3:
                self.handle_exit()

        elif isinstance(self.current_user,models.Admin):
            if choice == 1:
                self.show_all_products()
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

    




