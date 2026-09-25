import json
import models



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
        l = max(user['id'] for user in data['main_list'])
        uid = l + 1
    except ValueError:
        uid = 1
    d = {'id':uid,'name':name,'email':email,'password':pas,'location':loc}
    data['main_list'].append(d)

    with open(file,'w') as f:
        json.dump(data,f,indent=4)
    return True

def login(email,pas):
    with open('Data/users.json','r') as f:
        data = json.load(f)
    for user in data['main_list']:
        if user['email'] == email:
            if user['password'] == pas:
                print("Login Successfull") 
                u = models.User(user['id'],user['name'],email,pas,user['location'])
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
                u = models.Driver(driver['id'],driver['name'],email,pas,driver['location'])
                return u
            else:
                print("Wrong password entered")
                return False

    print("No email found Plz Signup")
    return False
