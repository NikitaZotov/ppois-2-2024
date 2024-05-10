from datetime import date
from time import struct_time

from src.main.model.entity.land_plot import LandPlot


class Building:
    def __init__(self, name: str, land_plot: LandPlot = None,
                 date_of_building: struct_time = None,
                 area_in_square_meters: float = 0.0,
                 floors: int = 1):
        self.__name = name
        self.__land_plot = land_plot
        self.__date_of_building = date_of_building
        self.__area_in_square_meters = area_in_square_meters
        self.__floors = floors

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, other: str) -> None:
        self.__name = other

    @property
    def land_plot(self) -> LandPlot:
        return self.__land_plot

    @land_plot.setter
    def land_plot(self, other: LandPlot) -> None:
        self.__land_plot = other

    @property
    def date_of_building(self) -> struct_time:
        return self.__date_of_building

    @date_of_building.setter
    def date_of_building(self, other: struct_time) -> None:
        self.__date_of_building = other

    @property
    def area_in_square_meters(self) -> float:
        return self.__area_in_square_meters

    @area_in_square_meters.setter
    def area_in_square_meters(self, other: float) -> None:
        self.__area_in_square_meters = other

    @property
    def floors(self) -> int:
        return self.__floors

    @floors.setter
    def floors(self, other: int) -> None:
        self.__floors = other

    def __str__(self):
        build_date = self.date_of_building
        day = build_date.tm_mday
        month = build_date.tm_mon
        year = build_date.tm_year
        return (f"Building[name='{self.name}', land_plot_cad_num='{self.land_plot.cadastral_number}', "
                f"date_of_building='{day}.{month}.{year}', "
                f"area_in_sq_m='{self.area_in_square_meters}'")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Building):
            return self.name == other.name
