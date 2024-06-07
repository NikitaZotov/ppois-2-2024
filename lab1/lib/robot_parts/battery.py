from lib.robot_parts.abс_robot_part import RobotPart


class Battery(RobotPart):
    def __init__(self):
        self._charge = 100

    def check_condition(self) -> bool:
        if self.charge <= 0:
            return False
        return True

    def fix_condition(self) -> None:
        self.recharge()

    @property
    def charge(self) -> int:
        return self._charge

    def get_low(self) -> None:
        if self.charge <= 0:
            raise ValueError("Battery low. Need recharge")
        self._charge -= 10

    def recharge(self) -> None:
        self._charge = 100
        print("Battery recharged")

    def __str__(self):
        return "battery"
