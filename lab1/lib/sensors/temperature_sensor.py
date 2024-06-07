from lib.cell import Cell
from lib.sensors.abс_sensor import Sensor


class TemperatureSensor(Sensor):
    def __init__(self):
        super().__init__()

    def measure_value(self, cell: Cell) -> None:
        self._current_value = cell.temperature

    def get_value(self) -> (str, int):
        if self._current_value is None:
            raise "Temperature must be measured before getting value"

        return "temperature", self._current_value
