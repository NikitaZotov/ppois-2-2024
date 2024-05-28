from unittest import TestCase

from equipment import Equipment


class TestEquipment(TestCase):
    def setUp(self):
        self.equipment: Equipment = Equipment(0)

    def test_price(self):
        self.equipment.price = 90
        self.assertEqual(self.equipment.price, 90)

    def test_use(self):
        self.equipment.use()
