import models


# Finance Related
finance = models.DB.load_finance()

def show_total_spent():
    return finance['total_spent']

def show_total_revenu():
    return finance['total_revenu']

def show_total_profits():
    return finance['total_profit']

def show_all_logs():
    return finance['logs']


# Orders Related

orders = models.DB.load_orders()


def get_total_orders():
    return len(orders)


def get_pending_orders():
    result = []
    for order in orders:
        if orders[order]['status'] == 'pending':
            result.append([ order,orders[order]['total'] ])
    return result


def get_delivered_orders():
    result = []
    for order in orders:
        if orders[order]['status'] == 'delivered':
            result.append([ order,orders[order]['total'] ])
    return result


def get_assigned_orders():
    result = []
    for order in orders:
        if orders[order]['status'] == 'assigned':
            result.append([ order,orders[order]['total'] ])
    return result


# Products Related

products = models.DB.load_products()


def total_number_of_products():
    return len(products['main_list'])


def get_low_stock_products():
    low_stock = []

    for product in products['main_list']:
        if product['quantity'] < 5:
            low_stock.append(product['id'])

    return low_stock


def get_out_of_stock_products():
    result = []

    for product in products['main_list']:
        if product['quantity'] == 0:
            result.append(product['id'])
    return result


def get_total_inventory_value():
    total = 0

    for product in products['main_list']:
        value = product['selling_price'] * product['quantity']
        total+=value 

    return total


def get_top_sold_products(n):
    sorted_products = sorted(finance['sold_products_count'], key=finance['sold_products_count'].get,reverse=True)

    result = []

    if len(sorted_products) >= n:
        for i in range(n):
            result.append(sorted_products[i])
    else:
        for i in sorted_products:
            result.append(i)

    return result


def most_sold_product():
    p = get_top_sold_products(1)
    return p


