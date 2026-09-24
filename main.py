import models

# result = models.Registration.sign_up('Ahmad','ahmad@gmail.com',1122,'Lahore','driver')
# print(result)


p = models.Product('Laptop',2000,2150,10)
p.save_product()
profit = p.sell_prod(6)
print(profit)