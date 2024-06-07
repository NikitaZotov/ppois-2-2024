from abc import ABC, abstractmethod


class Sensor(ABC):
    def __init__(self):
        self._current_value = None

    @abstractmethod
    def measure_value(self, cell) -> None:
        pass

    @abstractmethod
    def get_value(self) -> (str, int):
        pass
