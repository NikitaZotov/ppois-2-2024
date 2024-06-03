from classes.Participant import Participant
import unittest


class TestParticipant(unittest.TestCase):

    def test_constructor(self):
        participant = Participant(1, "Вика", 1000)
        self.assertEqual(participant.number, 1)
        self.assertEqual(participant.name, "Вика")
        self.assertEqual(participant.money, 1000)

    def test_name_setter(self):
        participant = Participant(1, "Вика", 1000)
        participant.name = "Cаша"
        self.assertEqual(participant.name, "Cаша")

    def test_money_setter(self):
        participant = Participant(1, "Вика", 1000)
        participant.money = 1100
        self.assertEqual(participant.money, 1100)

    def test_raise_price(self):
        participant = Participant(1, "Вика", 1000)
        price = participant.raise_price(100, 10)
        self.assertEqual(price, 110)

    def test_paid_money(self):
        participant = Participant(1, "Вика", 1000)
        participant.pay_money(900)
        self.assertEqual(participant.money, 100)

if __name__ == '__main__':
    unittest.main()
