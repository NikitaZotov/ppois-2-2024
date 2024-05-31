from src.main.model.entity.cadastral_number import CadastralNumber
from src.main.model.entity.land_plot import LandPlot
from src.main.model.entity.owner import Owner
from src.main.model.entity.enum.region import Region
from src.main.model.service.cadastral_agency import CadastralAgency
from src.main.controller.document_controller import DocumentController
from src.main.validator.land_plot_validator import LandPlotValidator
from src.main.view.menu import Menu


class LandController:
    def __init__(self):
        self._service = CadastralAgency()
        self._land_validator = LandPlotValidator()
        self._document_controller = DocumentController()

    def register_land_plot(self, valid_owner: Owner, current_region: Region) -> None:
        try:
            coordinates: tuple[float, float] = Menu.get_entry(self._land_validator.validate_coordinates,
                                                              "Enter characteristics for your land plot\n"
                                                              "Enter coordinates: ")
            area: float = Menu.get_entry(self._land_validator.validate_area, "Enter area in hectares: ")
            functional_purpose: str = self.__get_purpose()
            new_land_plot = LandPlot(coordinates, area, functional_purpose)
            self._service.register_land_plot(self.__give_cadastral_number(new_land_plot, current_region), valid_owner)
        except ValueError as e:
            Menu.show_error(str(e))

    def unregister_land_plot(self, valid_owner: Owner) -> None:
        try:
            land_to_unregister = self._document_controller.choose_land_plot_document(valid_owner,
                                                                                     "Choose a land to unregister")
            self._service.unregister_land_plot(land_to_unregister)
        except ValueError as e:
            Menu.show_error(str(e))

    def own_land_plot(self, valid_owner: Owner) -> None:
        unowned_land_plots = self._service.unregistered_land_plots
        Menu.print_menu(
            (
                "Choose the unowned land plot:"
            ),
            {
                **{str(i): lambda: self._service.register_land_plot(i, valid_owner) for i in unowned_land_plots},
                (0, "Back"): lambda: None
            }
        )
            
    def get_all_land_plots(self) -> None:
        if len(owned_lands := self._service.registered_land_plots) != 0:
            Menu.show_list(owned_lands, "---OWNED---")
        if len(unowned_lands := self._service.unregistered_land_plots) != 0:
            Menu.show_list(unowned_lands, "---UNOWNED---")
        
    def __get_purpose(self) -> str:

        def callback(input_):
            return input_

        return Menu.get_entry(callback, "Enter functional purpose: ")

    def __give_cadastral_number(self, valid_land: LandPlot, current_region: Region) -> LandPlot:
        while True:
            cad_block_num = self.__get_cad_block_num(current_region)
            land_plot_num = self.__get_land_plot_num()
            try:
                land_plot_num = int(land_plot_num)
                cad_block_num = int(cad_block_num)
                valid_land.cadastral_number = self._land_validator.validate_cadastral_number(
                    CadastralNumber(current_region,
                                    land_plot_num),
                    cad_block_num)
                break
            except ValueError as e:
                Menu.show_error(str(e))
        return valid_land

    def __get_land_plot_num(self) -> str:

        def callback(input_):
            return input_

        return Menu.get_entry(callback, "Enter land plot number:\n"
                                        f"(must be between 0 and 999999)\n")

    def __get_cad_block_num(self, current_region: Region) -> str:

        def callback(input_):
            return input_

        return Menu.get_entry(callback, f"Enter territorial block number:\n"
                                        f"(must be between 0 and {current_region.value['blocks']})\n")
