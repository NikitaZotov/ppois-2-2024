import unittest
from datetime import date, timedelta
from product import Product

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Яблоки", 2.5, date.today() + timedelta(days=10))
        self.expired_product = Product("Молоко", 3.0, date.today() - timedelta(days=1))

    def test_init(self):
        self.assertEqual(self.product.name, "Яблоки")
        self.assertEqual(self.product.price, 2.5)
        self.assertEqual(self.product.expiration_date, date.today() + timedelta(days=10))

    def test_is_expired(self):
        self.assertFalse(self.product.is_expired())
        self.assertTrue(self.expired_product.is_expired())

if __name__ == "__main__":
    unittest.main()