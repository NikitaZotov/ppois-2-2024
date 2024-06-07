from lib.cell import Cell
from lib.sensors.abс_sensor import Sensor


class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__()

    def measure_value(self, cell: Cell) -> None:
        self._current_value = cell.humidity

    def get_value(self) -> (str, int):
        if self._current_value is None:
            raise "Humidity must be measured before getting value"

        return "humidity", self._current_value

