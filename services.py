import models



def add_product(name,cp,sp,quan):

    bal = models.Admin.get_balance()
    cost = cp * quan
    if bal < cost:
        return False
    else:
        product = models.Product(name,cp,sp,quan)
        product.save_product()
        models.Admin.update_balance(bal-cost)

        
        return product


def restock_product(id,quan):
    bal = models.Admin.get_balance()
    products = models.DB.load_products()
    is_found = False
    for product in products['main_list']:
        if product['id'] == id:
            cp = product['cost_price']
            cost = cp * quan
            if bal >= cost:
                product['quantity']+=quan
                models.Admin.update_balance(bal - cost)
                models.DB.put_products(products)
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
                models.DB.put_products(products)
                models.Admin.update_balance(total)
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


        
    
                
