d  = [
    {'id':12,'price':14},
    {'id':13,'price':15},
    {'id':14,'price':16}
]


for i in d:
    if i['id'] == 13:
        i['price'] = 100


print(d)