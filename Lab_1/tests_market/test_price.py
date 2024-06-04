import unittest

from price import Price

class TestPrice(unittest.TestCase):
    def setUp(self):
        self.price = Price(100)

    def test_init(self):
        self.assertEqual(self.price.value, 100)

    def test_apply_discount(self):
        self.price.apply_discount(20)
        self.assertEqual(self.price.value, 80)
        
        self.price.apply_discount(50)
        self.assertEqual(self.price.value, 40)

        self.price.apply_discount(0)
        self.assertEqual(self.price.value, 40)

if __name__ == "__main__":
    unittest.main()