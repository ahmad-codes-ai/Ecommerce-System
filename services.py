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
            if admin_can_afford():
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

    if amount > balance:
        return True
    return False

add_product('Ahmad',100,120,10)

