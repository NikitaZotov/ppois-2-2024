from lib.cell import Cell
from lib.robot_parts.abс_robot_part import RobotPart


class Mechanism(RobotPart):
    def __init__(self):
        self._condition = True

    def check_condition(self) -> bool:
        return self._condition

    def fix_condition(self) -> None:
        self._condition = True

    def move(self, cell: Cell) -> None:
        if (cell.electrification > 50) or (cell.temperature > 50) or (cell.humidity > 50):
            self._condition = False

        if not self._condition:
            raise ValueError("Cell was dangerous. Mechanism was broken")

        print("Move's been done")

    def __str__(self):
        return "mechanism"
