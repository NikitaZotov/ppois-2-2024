from lib.cell import Cell
from lib.sensors.abс_sensor import Sensor


class ElectrificationSensor(Sensor):
    def __init__(self):
        super().__init__()

    def measure_value(self, cell: Cell) -> None:
        self._current_value = cell.electrification

    def get_value(self) -> (str, int):
        if self._current_value is None:
            raise "Electrification must be measured before getting value"

        return "electrification", self._current_value
