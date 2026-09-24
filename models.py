import json


class Registration():

    @staticmethod
    def sign_up(name,email,pas,loc,actor='user'):

        if actor == 'user':
            file = 'Data/users.json'
        else:
            file = 'Data/drivers.json'
        
        with open(file,'r') as f:
            data = json.load(f)

        for user in data["main_list"]:
            if user['email'] == email:
                return False
        try:
            l = max(data['main_list'])
            uid = l + 1
        except:
            uid = 1
        d = {'id':uid,'name':name,'email':email,'password':pas,'location':loc}
        data['main_list'].append(d)

        with open(file,'w') as f:
            json.dump(data,f,indent=4)
        return True

    @staticmethod
    def login(email,pas):
        with open('Data/users.json','r') as f:
            data = json.load(f)
        for user in data['main_list']:
            if user['email'] == email:
                if user['password'] == pas:
                    print("Login Successfull") 
                    u = User(user['id'],user['name'],email,pas,user['location'])
                    return u

                else:
                    print("Wrong Password entered")
                    return False

        with open('Data/drivers.json','r') as f:
            data = json.load(f)
        for driver in data['main_list']:
            if driver['email'] == email:
                if driver['password'] == pas:
                    print("Login Successfull")
                    u = Driver(driver['id'],driver['name'],email,pas,driver['location'])
                    return u
                else:
                    print("Wrong password entered")
                    return False

        print("No email found Plz Signup")
        return False


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

    



class Product():
    def __init__(self,name,cp,sp,quan=0):
        self.name = name
        self.cost_price = cp
        self.selling_price = sp
        self.quantity = quan 
        self.id = self.get_id()

    def get_id(self):
        with open('Data/products.json') as f:
            data = json.load(f)
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
        
        with open('Data/products.json','r') as f:
            data = json.load(f)

        data["main_list"].append(d)

        with open('Data/products.json','w') as f:
            json.dump(data,f,indent=4)


    def sell_prod(self,quan):
        if self.quantity >= quan:
            self.quantity-=quan
            profit = (quan * self.selling_price) - (quan * self.cost_price)

            with open('Data/products.json','r') as f:
                data = json.load(f)

            for prod in data['main_list']:
                if prod['id'] == self.id:
                    prod['quantity'] = self.quantity

            with open('Data/products.json','w') as f:
                json.dump(data,f,indent=4)
                return profit
        return False


