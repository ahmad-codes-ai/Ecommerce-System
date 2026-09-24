import models

# result = models.Registration.sign_up('Ahmad','ahmad@gmail.com',1122,'Lahore','driver')
# print(result)


r = models.Registration.login('ahmad@gmail.com',1122)
print(r.location)