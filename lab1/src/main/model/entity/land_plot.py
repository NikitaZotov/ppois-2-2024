from typing import Tuple


class LandPlot:
    def __init__(self, coordinates: tuple[float, float] = tuple[0.0, 0.0],
                 area_in_hectares: float = 0.0,
                 functional_purpose: str = ""):
        self.__cadastral_number = "000000000000000000"
        self.__coordinates = coordinates
        self.__area_in_hectares = area_in_hectares
        self.__functional_purpose = functional_purpose

    @property
    def cadastral_number(self) -> str:
        return self.__cadastral_number

    @cadastral_number.setter
    def cadastral_number(self, str_cadastral_number: str) -> None:
        self.__cadastral_number = str_cadastral_number

    @property
    def coordinates(self) -> tuple[float, float]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, coordinates: tuple[float, float]) -> None:
        self.__coordinates = coordinates

    @property
    def area_in_hectares(self) -> float:
        return self.__area_in_hectares

    @area_in_hectares.setter
    def area_in_hectares(self, area_in_hectares: float) -> None:
        self.__area_in_hectares = area_in_hectares

    @property
    def functional_purpose(self) -> str:
        return self.__functional_purpose

    @functional_purpose.setter
    def functional_purpose(self, functional_purpose: str) -> None:
        self.__functional_purpose = functional_purpose

    def __str__(self):
        return (f"LandPlot[cadastral_number='{self.cadastral_number}', coordinates='{self.coordinates}',"
                f" area_in_hectares='{self.area_in_hectares}', functional_purpose='{self.functional_purpose}']")

    def __eq__(self, other):
        return self.__cadastral_number == other.cadastral_number
