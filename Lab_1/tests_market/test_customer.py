import unittest
from unittest.mock import patch
from datetime import date, timedelta
from cart import Cart
from customer import Customer
from seller import Seller
from product import Product
from promotion import Promotion

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Джон", 1000)
        self.customer.cart = Cart()  
        self.seller = Seller("Алиса")
        expiration_date = date.today() + timedelta(days=30)
        self.product1 = Product("Хлеб", 10, expiration_date)
        self.product2 = Product("Молоко", 20, expiration_date)
        self.promotion1 = Promotion(self.product1.name, 20) 
        self.seller.products.extend([self.product1, self.product2])
        self.seller.promotions.append(self.promotion1)
        
   
if __name__ == '__main__':
    unittest.main()
