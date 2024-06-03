from classes.Lot import Lot
import unittest


class TestLot(unittest.TestCase):

    def test_constructor(self):
        lot = Lot("Кукла")
        self.assertEqual(lot.name, "Кукла")
        self.assertEqual(lot.start_price, 0)
        self.assertEqual(lot.bid, 0)

    def test_name_setter(self):
        lot = Lot("Кукла")
        lot.name = "Мяч"
        self.assertEqual(lot.name, "Мяч")

    def test_start_price_setter(self):
        lot = Lot("Кукла")
        lot.start_price = 100
        self.assertEqual(lot.start_price, 100)

    def test_bid_setter(self):
        lot = Lot("Кукла")
        lot.start_price = 100
        lot.bid = 10
        self.assertEqual(lot.bid, 10)

if __name__ == '__main__':
    unittest.main()
