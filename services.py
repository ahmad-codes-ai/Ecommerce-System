import models



def add_product(name,cp,sp,quan):
    cost = cp * quan
    bal = get_admin_balance()
    if admin_can_afford(cost):
        product = models.Product(name,cp,sp,quan)
        product.save_product()

        update_admin_balance(bal-cost)
        add_log_finance('add_prod',-cost)
        add_total_spent_finance(cost)
        return product
    return False


def restock_product(id,quan):
    bal = get_admin_balance()
    products = models.DB.load_products()
    for product in products['main_list']:
        if product['id'] == id:
            cp = product['cost_price']
            cost = cp * quan
            if admin_can_afford(cost):
                product['quantity']+=quan
                models.DB.put_products(products)

                update_admin_balance(bal - cost)
                add_log_finance('restock_prod',-cost)
                add_total_spent_finance(cost)
                return True
            else:
                return False



def sell_prod(id,quan):
    products = models.DB.load_products()

    for product in products['main_list']:
        if product['id'] == id:
            if product['quantity'] - quan > 0:
                product['quantity']-=quan
                total = product['selling_price'] * quan
                cost = product['cost_price'] * quan
                models.DB.put_products(products)

                update_admin_balance(get_admin_balance() + total)    
                put_sold_product(id,quan)
                add_revenu_finance(total)
                add_log_finance('sold_prod',total)
                add_profit_finance(total - cost)
                return True
            return False

        

def save_cart(customer):
    carts = models.DB.load_carts()

    carts[customer.id] = customer.cart

    models.DB.put_cart(carts)


def show_products():
    products = models.DB.load_products()
    print("ID \t \t Name \t \t \tPrice")
    for product in products['main_list']:
        print(f"{product['id']} \t \t {product['name']} \t \t {product['selling_price']}$")


def get_admin_balance():
    data = models.DB.load_admin()
    return data['balance']

def update_admin_balance(bal):
    data = models.DB.load_admin()
    data['balance'] = bal
    models.DB.put_admin(data)

def add_log_finance(task,amount):
    finance = models.DB.load_finance()
    d = {'task':task,'amount':amount}
    finance['logs'].append(d)
    models.DB.put_finance(finance)


def add_total_spent_finance(amount):
    finance = models.DB.load_finance()
    finance['total_spent']+=amount
    models.DB.put_finance(finance)


def add_profit_finance(amount):
    finance = models.DB.load_finance()
    finance['total_profit']+=amount
    models.DB.put_finance(finance)

def add_revenu_finance(amount):
    finance = models.DB.load_finance()
    finance['total_revenu']+=amount
    models.DB.put_finance(finance)

def admin_can_afford(amount):
    balance = get_admin_balance()

    if balance >= amount:
        return True
    return False


def get_product_sale_price(id):
    products = models.DB.load_products()

    for product in products['main_list']:
        if product['id'] == id:
            return product['selling_price']
    return False 


def get_product_cost_price(id):
    products = models.DB.load_products()

    for product in products['main_list']:
        if product['id'] == id:
            return product['cost_price']
    return False 

 
def get_cart_total(cart):
    total = 0
    for id,quan in cart:
        price = get_product_sale_price(id) * quan
        total+=price
    return total 


def get_cart_cost(cart):
    total = 0
    for id,quan in cart:
        price = get_product_cost_price(id) * quan
        total+=price
    return total



def checkout(customer):
    if len(customer.cart) > 0:

        # Order Related Logic
        orders = models.DB.load_orders()
        cart = customer.cart
        cart_total = get_cart_total(cart)
        cart_cost = get_cart_cost(cart)
        order_id = f"{customer.id}_{len(orders)}"
        d = {'products':cart,'total':cart_total,'status':'pending','driver_id':None,'city':customer.location}
        orders[order_id] = d
        customer.clear_cart()
        models.DB.put_orders(orders)

        # Selling and updating product and finance

        for id,quan in cart:
            result = sell_prod(id,quan)

        if result:
            return order_id
        
    return False


def product_exist(id):
    products = models.DB.load_products()

    for product in products['main_list']:
        if product['id'] == id:
            return True
    return False  


def get_product_stock(id):
    products = models.DB.load_products()

    for product in products['main_list']:
        if product['id'] == id:
            return product['quantity']
        return False


def show_all_orders(customer):
    id = customer.id

    orders = models.DB.load_orders()

    for order,details in orders.items():
        cust = order.split('_')
        if int(cust[0]) == id:
            print(f"{order} - {orders[order]['total']} - {orders[order]['status']}")



def show_order_details(id):
    orders = models.DB.load_orders()

    for order in orders:
        if order == id:
            return orders[order]
    return False


def put_sold_product(id,quan):
    finance = models.DB.load_finance()
    id = str(id)
    if id in finance['sold_products_count']:
        finance['sold_products_count'][id]+=quan
    else:
        finance['sold_products_count'][id] = quan
    models.DB.put_finance(finance)



# Driver Related Functions 

def get_orders_by_city(location):
    orders = models.DB.load_orders()
    result = []

    for order in orders:
        if orders[order]['city'].lower().strip() == location.lower().strip():
            result.append(order)
    return result



def show_order(id):
    orders = models.DB.load_orders()

    for order in orders:
        if order == id:
            print(orders[order])
            return True
    return False


def order_exist(id):
    orders = models.DB.load_orders()

    for order in orders:
        if order == id:
            return True
    return False


def get_order_status(id):
    if order_exist(id):
        orders = models.DB.load_orders()

        for order in orders:
            if order == id:
                return orders[order]['status']
    else:
        return False



def assign_driver_order(order_id,driver_id):
    orders = models.DB.load_orders()

    for order in orders:
        if order == order_id:
            if orders[order]['status'] == 'pending':
                orders[order]['status'] = 'assigned'
                orders[order]['driver_id'] = driver_id
    
    models.DB.put_orders(orders)


def get_driver_active_orders_count(id):
    orders = models.DB.load_orders()
    count = 0

    for order in orders:
        if order == id:
            count+=1
    return count


def get_driver_active_orders_details(id):
    orders = models.DB.load_orders()
    result = []

    for order in orders:
        if orders[order]['driver_id'] == id and orders[order]['status'] == 'assigned':
            result.append([order,[orders[order]['total']]])

    return result


def complete_delivery(order_id):
    orders = models.DB.load_orders()
    driver_earning = 7

    for order in orders:
        if order == order_id:
            orders[order]['status'] = 'delivered'  
            update_admin_balance(get_admin_balance() - driver_earning)
            add_log_finance('delivery_cost',-driver_earning)
            add_total_spent_finance(driver_earning)
            update_driver_earning(orders[order]['driver_id'],driver_earning)
    models.DB.put_orders(orders)
            

def update_driver_earning(id,amount):
    drivers = models.DB.load_drivers()
    
    for driver in drivers['main_list']:
        if driver['id'] == id:
            driver['earning']+=amount
            models.DB.put_drivers(drivers)
            return True
    return False 


def get_driver_earning(id):
    drivers = models.DB.load_drivers()

    for driver in drivers['main_list']:
        if driver['id'] == id:
            return driver['earning']
    return False


def get_completed_orders_rider(id):
    orders = models.DB.load_orders()
    result = []

    for order in orders:
        if orders[order]['driver_id'] == id:
            result.append([order,orders[order]['total']])

    return result
