import unittest
from lib.robot import Robot
from lib.cell_generator import CellGenerator
from lib.robot_parts.battery import Battery
from lib.robot_parts.software import Software
from lib.robot_parts.mechanism import Mechanism
from lib.sensors.humidity_sensor import HumiditySensor
from lib.sensors.temperature_sensor import TemperatureSensor
from lib.sensors.electrification_sensor import ElectrificationSensor


class TestRobot(unittest.TestCase):

    def setUp(self):
        self.robot = Robot()

    def test_robot_initialization(self):
        self.assertIsInstance(self.robot.battery, Battery)
        self.assertIsInstance(self.robot.software, Software)
        self.assertIsInstance(self.robot.mechanism, Mechanism)
        self.assertEqual(len(self.robot.sensors), 3)
        self.assertIsInstance(self.robot.sensors[0], ElectrificationSensor)
        self.assertIsInstance(self.robot.sensors[1], TemperatureSensor)
        self.assertIsInstance(self.robot.sensors[2], HumiditySensor)

    def test_robot_details(self):
        self.assertIn(self.robot.battery, self.robot.details)
        self.assertIn(self.robot.software, self.robot.details)

    def test_auto_move_successful(self):
        cells = CellGenerator.generate_cells()
        initial_battery_charge = self.robot.battery.charge

        self.robot.auto_move(1)

        # Проверяем, что батарея разрядилась
        self.assertLess(self.robot.battery.charge, initial_battery_charge)

    def test_auto_move_with_errors_and_auto_help(self):
        cells = CellGenerator.generate_cells()
        self.robot.software._errors_amount = 101  # Задаем количество ошибок, превышающее лимит

        # Пробуем вызвать auto_move и проверяем, что ошибка устраняется и move выполняется
        initial_battery_charge = self.robot.battery.charge

        self.robot.auto_move(1)

        self.assertEqual(self.robot.software._errors_amount, 0)  # Проверяем, что ошибки исправлены
        self.assertLess(self.robot.battery.charge, initial_battery_charge)

    def test_auto_move_negative_moves(self):
        with self.assertRaises(ValueError):
            self.robot.auto_move(-1)

    def test_show_cells(self):
        cells = CellGenerator.generate_cells()
        self.robot.show_cells(cells)  # Выводим клетки для ручной проверки


if __name__ == '__main__':
    unittest.main()
