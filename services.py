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

                update_admin_balance(total)
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


def admin_can_afford(amount):
    balance = get_admin_balance()

    if balance >= amount:
        return True
    return False


# All geteers from finance.json
def get_total_profit():
    finance = models.DB.load_finance()
    return finance['total_profit']

def get_total_revenu():
    finance = models.DB.load_finance()
    return finance['total_revenu']

def get_total_spending():
    finance = models.DB.load_finance()
    return finance['total_spent']

def get_total_logs():
    finance = models.DB.load_finance()
    return finance['logs']

def get_product_price(id):
    products = models.DB.load_products()

    for product in products['main_list']:
        if product['id'] == id:
            return product['selling_price']
    return False 


def get_cart_total(cart):
    total = 0
    for id,quan in cart:
        price = get_product_price(id) * quan
        total+=price
    return total 


def checkout(customer):
    orders = models.DB.load_orders()
    cart = customer.cart
    total = get_cart_total(cart)
    order_id = f"{customer.id}_{len(orders)}"
    d = {'products':cart,'total':total,'status':'pending','driver_id':None}
    orders[order_id] = d
    models.DB.put_orders(orders)



cust = models.User(101,'cust','cust@gmail.com',1111,'lahore')

cust.add_item_to_cart(1,4)
checkout(cust)

