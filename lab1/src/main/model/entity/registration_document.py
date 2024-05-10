from datetime import date
from abc import ABC, abstractmethod
from src.main.model.entity.owner import Owner
from src.main.model.entity.land_plot import LandPlot
from src.main.model.entity.building import Building


class RegistrationDocument(ABC):
    def __init__(self, owner: Owner, registration_date: date):
        self._owner = owner
        self._registration_date = registration_date

    def __str__(self):
        return (f"Owner: {self._owner.passport_id}|{self._owner.first_name[0]}.{self._owner.last_name}\n"
                f"Registration date: {self._registration_date}")

    @abstractmethod
    def short_desc(self) -> str: pass

    @property
    def owner(self) -> Owner:
        return self._owner

    def update(self):
        self._registration_date = date.today()

    def __eq__(self, other):
        if isinstance(other, RegistrationDocument):
            return self._owner == other._owner


class LandRegistrationDocument(RegistrationDocument):

    def __init__(self, owner: Owner, registration_date: date, land_plot: LandPlot):
        super().__init__(owner, registration_date)
        self.__land_plot = land_plot

    def short_desc(self) -> str:
        return f"LAND|{self._registration_date}|CAD_NUM:'{self.__land_plot.cadastral_number}'"

    @property
    def land_plot(self) -> LandPlot:
        return self.__land_plot

    def __str__(self):
        return (super().__str__()
                + f"\nCAD_NUM: {self.__land_plot.cadastral_number}"
                  f"\nCOORDINATES: {self.__land_plot.coordinates}"
                  f"\nAREA: {self.__land_plot.area_in_hectares} hectares")

    def __eq__(self, other):
        if isinstance(other, LandRegistrationDocument):
            return self._owner == other._owner and self.land_plot == other.land_plot


class BuildingRegistrationDocument(RegistrationDocument):
    def __init__(self, owner: Owner, registration_date: date, building: Building):
        super().__init__(owner, registration_date)
        self.__building = building

    def short_desc(self) -> str:
        return f"BUILDING|{self._registration_date}|BUILDING_NAME:'{self.__building.name}'"

    @property
    def building(self) -> Building:
        return self.__building

    def __str__(self):
        build_date = self.__building.date_of_building
        day = build_date.tm_mday
        month = build_date.tm_mon
        year = build_date.tm_year
        return (super().__str__()
                + f"\nNAME: {self.__building.name}"
                  f"\nAREA: {self.__building.area_in_square_meters} sq.m."
                  f"\nFLOORS: {self.__building.floors}"
                  f"\nLAND_PLOT_CAD_NUM: {self.__building.land_plot.cadastral_number}"
                  f"\nDATE_OF_BUILDING: {day}.{month}.{year}")

    def __eq__(self, other):
        if isinstance(other, BuildingRegistrationDocument):
            return self._owner == other._owner and self.building == other.building