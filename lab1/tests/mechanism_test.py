import unittest
from lib.cell import Cell
from lib.robot_parts.mechanism import Mechanism

class TestMechanism(unittest.TestCase):

    def setUp(self):
        self.mechanism = Mechanism()

    def test_initial_condition(self):
        self.assertTrue(self.mechanism.check_condition())

    def test_fix_condition(self):
        self.mechanism._condition = False
        self.mechanism.fix_condition()
        self.assertTrue(self.mechanism.check_condition())

    def test_move_safe_cell(self):
        safe_cell = Cell(electrification=40, temperature=30, humidity=20)
        self.mechanism.move(safe_cell)
        self.assertTrue(self.mechanism.check_condition())

    def test_move_dangerous_cell(self):
        dangerous_cell = Cell(electrification=60, temperature=60, humidity=60)
        with self.assertRaises(ValueError):
            self.mechanism.move(dangerous_cell)
        self.assertFalse(self.mechanism.check_condition())

    def test_str_representation(self):
        self.assertEqual(str(self.mechanism), "mechanism")


if __name__ == '__main__':
    unittest.main()
