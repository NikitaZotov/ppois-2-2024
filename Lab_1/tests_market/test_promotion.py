import unittest
from promotion import Promotion

class TestPromotion(unittest.TestCase):
    def setUp(self):
        self.promotion = Promotion("Яблоки", 20)

    def test_apply_discount(self):
        discounted_price = self.promotion.apply_discount(10.0)
        self.assertAlmostEqual(discounted_price, 8.0, places=2)

    def test_promotion_data(self):
        self.assertEqual(self.promotion.product_name, "Яблоки")
        self.assertEqual(self.promotion.discount_percent, 20)

if __name__ == "__main__":
    unittest.main()
