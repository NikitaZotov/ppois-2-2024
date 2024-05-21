import unittest
from datetime import date, timedelta
from seller import Seller
from product import Product
from promotion import Promotion

class TestSeller(unittest.TestCase):
    def setUp(self):
        self.seller = Seller("Магазин АБВ")
        self.seller.add_product("Яблоко", 2.5, str(date.today() + timedelta(days=10)))
        self.seller.add_product("Банан", 1.5, str(date.today() + timedelta(days=20)))
        self.seller.add_promotion("Яблоко", 20)

    def test_expired_product(self):
        self.seller.add_product("Молоко", 3.0, str(date.today() - timedelta(days=1)))
        self.assertIsNone(self.seller.find_product("Молоко"))

    def test_promotion(self):
        promotion = self.seller.find_promotion("Яблоко")
        self.assertIsNotNone(promotion)
        self.assertEqual(promotion.discount_percent, 20)
        discounted_price = promotion.apply_discount(2.5)
        self.assertAlmostEqual(discounted_price, 2.0, places=2)

if __name__ == "__main__":
    unittest.main()
