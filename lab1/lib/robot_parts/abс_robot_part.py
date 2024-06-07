from abc import ABC, abstractmethod


class RobotPart(ABC):
    @abstractmethod
    def check_condition(self) -> bool:
        pass

    def fix_condition(self) -> None:
        pass
