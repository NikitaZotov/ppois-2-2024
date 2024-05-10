from time import strptime, struct_time

from src.main.model.entity.building import Building
from src.main.model.entity.land_plot import LandPlot
from src.main.model.entity.owner import Owner
from src.main.model.service.cadastral_agency import CadastralAgency
from src.main.controller.document_controller import DocumentController
from src.main.validator.building_validator import BuildingValidator
from src.main.view.menu import Menu


class BuildingController:
    def __init__(self):
        self._service = CadastralAgency()
        self._building_validator = BuildingValidator()
        self._document_controller = DocumentController()

    def register_building(self, valid_owner: Owner) -> None:
        try:
            land_plot: LandPlot = (self
                                   ._document_controller
                                   .choose_land_plot_document(valid_owner,
                                                              "Choose a land plot to register "
                                                              "your building on\n"
                                                              f"{valid_owner.first_name[0]}.{valid_owner.last_name}"
                                                              f"'s Land Documents").land_plot)
            building_name: str = Menu.get_entry(self._building_validator.validate_building_name,
                                                "Enter building name: ")
            date_of_building: struct_time = Menu.get_entry(self.__get_time, "Enter date of building: [DD.MM.YYYY]\n")
            building_area: float = self.__get_area(land_plot)
            floors: int = Menu.get_entry(self._building_validator.validate_floors, "Enter number of floors: ")
            self._service.register_building(Building(building_name, land_plot, date_of_building,
                                                     building_area, floors), valid_owner)
        except ValueError as e:
            Menu.show_error(str(e))

    def unregister_building(self, valid_owner: Owner) -> None:
        try:
            build_doc = self._document_controller.choose_building_document(valid_owner,
                                                                           "Choose building to unregister")
            self._service.unregister_building(build_doc)
        except ValueError as e:
            Menu.show_error(str(e))

    def get_all_buildings(self) -> None:
        Menu.show_list(self._service.registered_buildings, "Buildings")

    def __get_time(self, input_: str):
        return strptime(input_, "%d.%m.%Y")

    def __get_area(self, land_plot: LandPlot):

        def callback(input_: str):
            return input_

        return self._building_validator.validate_area_in_square_meters(
            Menu.get_entry(callback, "Enter building area in square meters:"
                                     f"({self._service.get_land_plot_left_area(land_plot)} sq.m. left)\n"),
            land_plot)
