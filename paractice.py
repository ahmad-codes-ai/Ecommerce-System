import json
import models
import services

u = models.User(1,'ahmad','user@gmail.com',1122,'lahore')
result = models.User.add_item_to_cart(u,1,2)
# services.save_cart(u)
print(result)
print(u.cart)
