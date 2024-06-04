import unittest
from market import Market
from customer import Customer
from seller import Seller

class TestMarket(unittest.TestCase):
    def setUp(self):
        self.market = Market()
        self.customer = Customer("Иван Иванов", 1000)
        self.seller = Seller("Алиса")

    def test_add_customer(self):
        self.market.add_customer(self.customer)
        self.assertIn(self.customer, self.market.customers)

    def test_find_customer(self):
        self.market.add_customer(self.customer)
        found_customer = self.market.find_customer("Иван Иванов")
        self.assertEqual(found_customer, self.customer)
        not_found_customer = self.market.find_customer("Петр Петров")
        self.assertIsNone(not_found_customer)

    def test_add_seller(self):
        self.market.add_seller(self.seller)
        self.assertIn(self.seller, self.market.sellers)

    def test_find_seller(self):
        self.market.add_seller(self.seller)
        found_seller = self.market.find_seller("Алиса")
        self.assertEqual(found_seller, self.seller)
        not_found_seller = self.market.find_seller("Ваня")
        self.assertIsNone(not_found_seller)

if __name__ == "__main__":
    unittest.main()
