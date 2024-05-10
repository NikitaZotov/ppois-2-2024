import re
from src.main.model.entity.land_plot import LandPlot
from src.main.model.service.cadastral_agency import CadastralAgency


class BuildingValidator:
    def __init__(self):
        self._service = CadastralAgency()

    def validate_building_name(self, name: str) -> str:
        if name not in [i.name for i in self._service.registered_buildings]:
            return name
        else:
            raise ValueError("Name is not valid or already exists")

    def validate_area_in_square_meters(self, str_area: str, land_plot: LandPlot) -> float:
        area = float(str_area)
        if area <= 0:
            raise ValueError("Area is not valid")
        elif (left_area := self._service.get_land_plot_left_area(land_plot)) < area:
            raise ValueError(f"This land has {left_area} sq.meters left")
        return area

    def validate_floors(self, str_floors: str) -> int:
        if int(str_floors) <= 0:
            raise ValueError("Floors are not valid")
        return int(str_floors)
