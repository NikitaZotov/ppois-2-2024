import unittest
from cart import Cart

class TestCart(unittest.TestCase):

    def setUp(self):
        self.cart = Cart()

    def test_add_item_and_calculate_total(self):
        self.cart.add_item('Алиса', 'Сухари', 2, 10)
        self.cart.add_item('Виктор', 'Мука', 3, 15)
        self.assertEqual(self.cart.calculate_total(), 65)

    def test_clear_cart(self):
        self.cart.add_item('Алиса', 'Сухари', 2, 10)
        self.cart.clear()
        self.assertEqual(len(self.cart.items), 0)

if __name__ == '__main__':
    unittest.main()
