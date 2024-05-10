from typing import Callable

from src.main.model.entity.enum.region import Region
from src.main.model.service.cadastral_agency import CadastralAgency
from src.main.controller.building_controller import BuildingController
from exception import BackException
from src.main.controller.document_controller import DocumentController
from src.main.controller.land_controller import LandController
from src.main.controller.owner_controller import OwnerController
from src.main.view.menu import Menu


class CadastralAgencyController:
    def __init__(
            self,
            service: CadastralAgency = CadastralAgency(),
            owner_controller: OwnerController = OwnerController(),
            land_controller: LandController = LandController(),
            document_controller: DocumentController = DocumentController(),
            building_controller: BuildingController = BuildingController(),
    ):
        self._service = service
        self._owner_controller = owner_controller
        self._land_controller = land_controller
        self._document_controller = document_controller
        self._building_controller = building_controller

    def select_region(self, current_region: Region) -> Region:
        chosen_region: Region = Region.DEFAULT

        def select_reg(reg):
            nonlocal chosen_region
            chosen_region = reg

        regs_without_default: list[Region] = []
        for re in Region:
            if re is not Region.DEFAULT:
                regs_without_default.append(re)
        action_dict: dict[str | tuple[int, str], Callable] \
            = {**{r.name: (lambda r=r: select_reg(r)) for r in regs_without_default}}
        if current_region != Region.DEFAULT:
            action_dict[(0, "Back")] = lambda r=current_region: select_reg(r)
        while chosen_region is Region.DEFAULT:
            Menu.print_menu("Region Selection", action_dict)
        return chosen_region

    def land_plot_registration(self, current_region: Region) -> None:
        if (owner := self._owner_controller.check_owner()) is None:
            print("Cancelled!")
            return
        back_flag = False

        def back():
            nonlocal back_flag
            back_flag = True

        while not back_flag:
            try:
                Menu.print_menu("Land Plot Registration",
                                {
                                    "Register Land Plot": lambda: self._land_controller.register_land_plot(owner,
                                                                                                           current_region),
                                    "Unregister Land Plot": lambda: self._land_controller.unregister_land_plot(owner),
                                    "Pick Unowned Land Plot": lambda: self._land_controller.own_land_plot(owner),
                                    (0, "Back"): lambda: back()
                                })
            except BackException:
                pass

    def building_registration(self):
        if (owner := self._owner_controller.check_owner()) is None:
            print("Cancelled!")
            return
        back_flag = False

        def back():
            nonlocal back_flag
            back_flag = True

        while not back_flag:
            try:
                Menu.print_menu("Building Registration",
                                {
                                    "Register Building": lambda: self._building_controller.register_building(owner),
                                    "Unregister Building": lambda: self._building_controller.unregister_building(owner),
                                    (0, "Back"): lambda: back()
                                })
            except BackException:
                pass

    def information_presentation(self):
        back_flag = False

        def back():
            nonlocal back_flag
            back_flag = True

        while not back_flag:
            Menu.print_menu("information & Documents",
                            {
                                "Show All Land Plots": lambda: self._land_controller.get_all_land_plots(),
                                "Show All Buildings": lambda: self._building_controller.get_all_buildings(),
                                "Show All Owner's Registrations":
                                    lambda: self._document_controller.get_all_documents_of_owner(
                                        self._owner_controller.check_owner()),
                                (0, "Back"): lambda: back()
                            })

    def save_all(self):
        self._service.save_all()

    def load(self):
        self._service.load()
