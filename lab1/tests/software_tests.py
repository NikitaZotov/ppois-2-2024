# test_software.py
import unittest
from unittest.mock import Mock, patch
from lib.robot_parts.software import Software
from lib.cell import Cell
from lib.sensors.abс_sensor import Sensor


class TestSoftware(unittest.TestCase):
    def setUp(self):
        self.software = Software()
        self.mock_sensor = Mock(spec=Sensor)
        self.mock_cell = Mock(spec=Cell)

    def test_initial_top_limits(self):
        expected_limits = {"electrification": 100, "temperature": 100, "humidity": 100}
        self.assertEqual(self.software.top_limits, expected_limits)

    def test_check_condition_initial(self):
        self.assertTrue(self.software.check_condition())

    def test_check_condition_after_errors(self):
        self.software._errors_amount = 101
        self.assertFalse(self.software.check_condition())

    def test_fix_condition(self):
        self.software._errors_amount = 50
        self.software.fix_condition()
        self.assertEqual(self.software._errors_amount, 0)

    def test_stats_difference(self):
        stats = {"electrification": 110, "temperature": 95, "humidity": 105}
        self.assertEqual(self.software.stats_difference(stats), 15)

    def test_get_cell_stats(self):
        self.mock_sensor.get_value.return_value = ("temperature", 50)
        stats = Software.get_cell_stats([self.mock_sensor], self.mock_cell)
        self.assertEqual(stats, {"temperature": 50})

    def test_update_limits(self):
        new_limits = {"electrification": 120, "temperature": 80, "humidity": 110}
        self.software.update_limits(new_limits)
        self.assertEqual(self.software._top_limits, {"electrification": 120, "temperature": 100, "humidity": 110})

    def test_collect_errors(self):
        with patch('lib.robot_parts.software.Software.generate_error_probability', return_value=5):
            self.software.collect_errors()
            self.assertEqual(self.software._errors_amount, 5)

    def test_generate_error_probability(self):
        # This test will not be deterministic due to the random nature of the method
        prob = Software.generate_error_probability()
        self.assertTrue(0 <= prob <= 40)

    def test_choose_cell(self):
        # Setup mock sensors and cells
        self.mock_sensor.get_value.side_effect = [("temperature", 50), ("humidity", 50)]
        cell1 = Mock(spec=Cell)
        cell2 = Mock(spec=Cell)
        cells = [cell1, cell2]

        # Choose cell should pick the best match based on sensor stats
        chosen_cell = self.software.choose_cell([self.mock_sensor], cells)
        self.assertIn(chosen_cell, cells)

    def test_choose_cell_with_errors(self):
        self.software._errors_amount = 101
        with self.assertRaises(ValueError):
            self.software.choose_cell([self.mock_sensor], [self.mock_cell])


if __name__ == '__main__':
    unittest.main()
