# import json
# import models
# import services

# u = models.User(1,'ahmad','user@gmail.com',1122,'lahore')
# result = models.User.add_item_to_cart(u,1,2)
# resul2 = models.User.add_item_to_cart(u,1,4)
# models.User.remove_item_from_cart(u,1)
# # services.save_cart(u)
# print(result)
# print(u.cart)


order_id = 1111
def x(y):
    if y > 2:
        return order_id
    else:
        return False

result = x(1)


if result:
    print(result)
else:
    print("Not result")
