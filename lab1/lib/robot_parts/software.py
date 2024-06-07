import random

from lib.cell import Cell
from lib.sensors.abс_sensor import Sensor
from lib.robot_parts.abс_robot_part import RobotPart


class Software(RobotPart):
    def __init__(self):
        self._errors_amount = 0
        self._top_limits = {"electrification": 100, "temperature": 100, "humidity": 100}

    @property
    def top_limits(self) -> dict:
        return self._top_limits.copy()

    def check_condition(self) -> bool:
        if self._errors_amount > 100:
            return False
        return True

    def fix_condition(self) -> None:
        self._errors_amount = 0

    def choose_cell(self, sensors: list[Sensor], cells: list[Cell]) -> Cell:
        if not self.check_condition():
            raise ValueError("To many errors in robot software. You need to fix them")

        res_dif, res_cell = float('inf'), None
        for cell in cells:
            stats = Software.get_cell_stats(sensors, cell)
            dif = self.stats_difference(stats)

            if dif <= 0:
                self.collect_errors()
                return cell

            if dif < res_dif:
                res_dif, res_cell = dif, cell

        self.update_limits(Software.get_cell_stats(sensors, res_cell))
        self.collect_errors()
        return res_cell

    def stats_difference(self, stats: dict) -> int:
        return sum(stats[key] - self.top_limits[key] for key in stats if stats[key] > self.top_limits[key])

    @staticmethod
    def get_cell_stats(sensors: list[Sensor], cell: Cell) -> dict:
        stats = dict()
        for sensor in sensors:
            sensor.measure_value(cell)
            info = sensor.get_value()
            stats[info[0]] = info[1]
        return stats

    def update_limits(self, limits: dict) -> None:
        for limit, value in limits.items():
            self._top_limits[limit] = max(value, self._top_limits[limit])

    def collect_errors(self) -> None:
        self._errors_amount += Software.generate_error_probability()

    @staticmethod
    def generate_error_probability() -> int:
        total_probability = 1.0
        current_number = 40

        while True:
            current_probability = total_probability / (current_number + 1)

            if random.random() < current_probability:
                return current_number

            total_probability -= current_probability
            current_number -= 1

            if current_number < 0:
                return 0

    def __str__(self):
        return "software"
