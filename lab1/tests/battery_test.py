import unittest
from lib.robot_parts.battery import Battery

class TestBattery(unittest.TestCase):

    def setUp(self):
        self.battery = Battery()

    def test_initial_charge(self):
        self.assertEqual(self.battery.charge, 100)

    def test_check_condition_initial(self):
        self.assertTrue(self.battery.check_condition())

    def test_get_low(self):
        self.battery.get_low()
        self.assertEqual(self.battery.charge, 90)

    def test_get_low_until_empty(self):
        for _ in range(10):
            self.battery.get_low()
        self.assertEqual(self.battery.charge, 0)
        self.assertFalse(self.battery.check_condition())
        with self.assertRaises(ValueError):
            self.battery.get_low()

    def test_recharge(self):
        self.battery.get_low()
        self.battery.recharge()
        self.assertEqual(self.battery.charge, 100)

    def test_fix_condition(self):
        for _ in range(10):
            self.battery.get_low()
        self.battery.fix_condition()
        self.assertEqual(self.battery.charge, 100)

    def test_str_representation(self):
        self.assertEqual(str(self.battery), "battery")


if __name__ == '__main__':
    unittest.main()
