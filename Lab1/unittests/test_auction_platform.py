from classes.AuctionPlatform import AuctionPlatform
import unittest


class TestAuctionPlatform(unittest.TestCase):

    def test_constructor(self):
        auction = AuctionPlatform()
        self.assertEqual(auction.count_lots(), 0)
        self.assertEqual(auction.count_participants(), 0)
        self.assertEqual(auction.time, 300)

    def test_list_participant_getter(self):
        auction = AuctionPlatform()
        self.assertEqual(auction.list_of_participants, [])

    def test_add_lot(self):
        auction = AuctionPlatform()
        auction.add_lot("Кукла", 1000, 100)
        self.assertEqual(auction.count_lots(), 1)
        self.assertEqual(auction.count_participants(), 0)
        self.assertEqual(auction.time, 300)

    def test_add_participant(self):
        auction = AuctionPlatform()
        auction.add_participant("Вика", 10000)
        self.assertEqual(auction.count_lots(), 0)
        self.assertEqual(auction.count_participants(), 1)
        self.assertEqual(auction.time, 300)

    def test_install_timer(self):
        auction = AuctionPlatform()
        auction.install_timer(10)
        self.assertEqual(auction.count_lots(), 0)
        self.assertEqual(auction.count_participants(), 0)
        self.assertEqual(auction.time, 10)

if __name__ == '__main__':
    unittest.main()
