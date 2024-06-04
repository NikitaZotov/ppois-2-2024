import datetime

class Product:
    def __init__(self, name, price, expiration_date):
        self.name = name
        self.price = price
        self.expiration_date = expiration_date

    def is_expired(self):
        return self.expiration_date < datetime.date.today()

x = 34.4 
print(tyx)