import unittest
from lib.cell import Cell
from lib.sensors.electrification_sensor import ElectrificationSensor
from lib.sensors.humidity_sensor import HumiditySensor
from lib.sensors.temperature_sensor import TemperatureSensor


class TestSensors(unittest.TestCase):

    def setUp(self):
        self.cell = Cell(electrification=50, humidity=30, temperature=25)

    def test_electrification_sensor(self):
        sensor = ElectrificationSensor()
        sensor.measure_value(self.cell)
        self.assertEqual(sensor.get_value(), ("electrification", 50))

    def test_humidity_sensor(self):
        sensor = HumiditySensor()
        sensor.measure_value(self.cell)
        self.assertEqual(sensor.get_value(), ("humidity", 30))

    def test_temperature_sensor(self):
        sensor = TemperatureSensor()
        sensor.measure_value(self.cell)
        self.assertEqual(sensor.get_value(), ("temperature", 25))

    def test_electrification_sensor_without_measure(self):
        sensor = ElectrificationSensor()
        with self.assertRaises(Exception):
            sensor.get_value()

    def test_humidity_sensor_without_measure(self):
        sensor = HumiditySensor()
        with self.assertRaises(Exception):
            sensor.get_value()

    def test_temperature_sensor_without_measure(self):
        sensor = TemperatureSensor()
        with self.assertRaises(Exception):
            sensor.get_value()


if __name__ == '__main__':
    unittest.main()
