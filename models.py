import json


class Map():
    cities = ['lahore','islamabad','karachi']
    distances = {
        # Lahore connections
        'lahore-islamabad': 377,
        'islamabad-lahore': 377,
        'lahore-karachi': 1203,
        'karachi-lahore': 1203,
        'lahore-multan': 405,
        'multan-lahore': 405,
        
        # Islamabad connections
        'islamabad-karachi': 1405,
        'karachi-islamabad': 1405,
        'islamabad-multan': 544,
        'multan-islamabad': 544,
        
        # Karachi & Multan connection
        'karachi-multan': 877,
        'multan-karachi': 877
    }

class User():
    def __init__(self,id,name,email,pas,loc):
        self.id = id
        self.name = name
        self.email = email
        self.password = pas 
        self.location = loc
        self.cart = []

    def add_item_to_cart(self,id,quan):
        products = DB.load_products()

        for product in products['main_list']:
            if product['id'] == id:
                if product['quantity'] >= quan:
                    detail = [id,quan]
                    self.cart.append(detail)
                    return True
                return False

    def view_cart(self):
        carts = DB.load_carts()
        data = carts.get(self.id)
        return data

    def remove_item_from_cart(self,id):
        idx = 0
        self.cart = [item for item in self.cart if item['id']!=id]


    def checkout(self):
        pass


class Driver():
    def __init__(self,id,name,email,pas,loc):
        self.id = id
        self.name = name
        self.email = email
        self.password = pas 
        self.location = loc
        self.balance = 0
        self.status = None

class Admin():
    def __init__(self,name,email,pas,bal=0):
        self.name = name
        self.email = email
        self.password = pas
        self.balance = bal

    def get_balance(self):
        return self.balance

    def update_balance(self,bal):
        self.balance = bal

    def update_file_balance(self):
        pass


    



class Product():
    def __init__(self,name,cp,sp,quan=0):
        self.name = name
        self.cost_price = cp
        self.selling_price = sp
        self.quantity = quan 
        self.id = self.get_id()

    def get_id(self):
        data = DB.load_products()
        try:
            l = max(data["main_list"])
            return l+1
        except:
            return 1
    def save_product(self):

        d = {'name': self.name,
             'cost_price': self.cost_price,
             'selling_price': self.selling_price,
             'quantity': self.quantity,
             'id': self.id}
        
        data = DB.load_products()

        data["main_list"].append(d)

        DB.put_products(data)


class DB():

    @staticmethod
    def load_products():
        with open('Data/products.json','r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_drivers():
        with open('Data/drivers.json','r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_users():
        with open('Data/users.json','r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_finance():
        with open('Data/finance.json','r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_carts():
        with open('Data/carts.json','r') as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def put_products(data):
        with open('Data/products.json','w') as f:
            json.dump(data,f,indent=4)

    @staticmethod
    def put_drivers(data):
        with open('Data/drivers.json','w') as f:
            json.dump(data,f,indent=4)

    @staticmethod
    def put_users(data):
        with open('Data/users.json','w') as f:
            json.dump(data,f,indent=4)

    @staticmethod
    def put_cart(data):
        with open('Data/carts.json','w') as f:
            json.dump(data,f,indent=4)




