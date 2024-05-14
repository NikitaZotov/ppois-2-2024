from classes.Bid import Bid
import unittest


class TestBid(unittest.TestCase):

    def test_constructor(self):
        bid = Bid(100)
        self.assertEqual(bid.get_bid(), 100)

    def test_bid_setter(self):
        bid = Bid(100)
        bid.set_bid(10)
        self.assertEqual(bid.get_bid(), 10)

if __name__ == '__main__':
    unittest.main()
