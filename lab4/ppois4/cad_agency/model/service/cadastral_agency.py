from typing import List
from datetime import date

from cad_agency.model.entity.building import Building
from cad_agency.model.entity.enum.region import Region
from cad_agency.model.entity.land_plot import LandPlot
from cad_agency.model.entity.owner import Owner
from cad_agency.model.entity.registration_document import RegistrationDocument, LandRegistrationDocument, \
    BuildingRegistrationDocument
from cad_agency.model.serialize.shelve_serializer import ShelveSerializer


class CadastralAgencyMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CadastralAgency(metaclass=CadastralAgencyMeta):
    def __init__(self):
        self.__serializer = ShelveSerializer()
        self.__documents = []
        self.__registered_owners = []
        self.__registered_buildings = []
        self.__registered_land_plots = []
        self.__unregistered_land_plots = []
        self.__current_region: Region = Region.DEFAULT

    @property
    def documents(self) -> List[RegistrationDocument]:
        return self.__documents

    @property
    def registered_owners(self) -> List[Owner]:
        return self.__registered_owners

    @property
    def registered_buildings(self) -> List[Building]:
        return self.__registered_buildings

    @property
    def registered_land_plots(self) -> List[LandPlot]:
        return self.__registered_land_plots

    @property
    def unregistered_land_plots(self) -> List[LandPlot]:
        return self.__unregistered_land_plots

    @property
    def current_region(self) -> Region:
        return self.__current_region

    @current_region.setter
    def current_region(self, region: Region):
        self.__current_region = region

    def register_land_plot(self, valid_land: LandPlot, land_owner: Owner) -> None:
        new_land_document = LandRegistrationDocument(land_owner, date.today(), valid_land)
        self.documents.append(new_land_document)
        self.registered_land_plots.append(valid_land)
        if valid_land in self.unregistered_land_plots:
            self.unregistered_land_plots.remove(valid_land)

    def unregister_land_plot(self, document: LandRegistrationDocument) -> None:
        self.unregistered_land_plots.append(document.land_plot)
        self.registered_land_plots.remove(document.land_plot)
        self.__clear_building_registrations(document.land_plot)
        self.documents.remove(document)

    def register_building(self, valid_building: Building, building_owner: Owner) -> None:
        new_building_document = BuildingRegistrationDocument(building_owner, date.today(), valid_building)
        self.documents.append(new_building_document)
        self.registered_buildings.append(valid_building)

    def unregister_building(self, document: BuildingRegistrationDocument) -> None:
        self.registered_buildings.remove(document.building)
        self.documents.remove(document)

    def register_owner(self, valid_owner: Owner) -> Owner:
        self.registered_owners.append(valid_owner)
        return valid_owner

    def get_land_plot_left_area(self, land_plot: LandPlot) -> float:
        area_left = land_plot.area_in_hectares * 10000
        for building in self.registered_buildings:
            if building.land_plot == land_plot:
                area_left -= building.area_in_square_meters
        return area_left

    def load(self, file_path: str = ""):
        shelf = self.__serializer.deserialize()
        if file_path != "":
            self.__serializer.save_file_path = file_path
        try:
            self.__documents = shelf["documents"]
            self.__registered_owners = shelf["owners"]
            self.__registered_buildings = shelf["buildings"]
            self.__registered_land_plots = shelf["land_plots"]
            self.__unregistered_land_plots = shelf["u_land_plots"]
        except KeyError:
            pass

    def save_all(self, file_path: str = "") -> None:
        if file_path != "":
            self.__serializer.save_file_path = file_path
        self.__serializer.serialize(owners=self.registered_owners,
                                    buildings=self.registered_buildings,
                                    land_plots=self.registered_land_plots,
                                    u_land_plots=self.unregistered_land_plots,
                                    documents=self.documents)

    def __clear_building_registrations(self, land_plot: LandPlot) -> None:
        for building in self.registered_buildings.copy():
            if building.land_plot == land_plot:
                self.registered_buildings.remove(building)
                for document in self.documents:
                    if isinstance(document, BuildingRegistrationDocument) and document.building == building:
                        self.documents.remove(document)

    def get_owner_land_documents(self, valid_owner: Owner) -> list[LandRegistrationDocument]:
        land_doc_list: list[LandRegistrationDocument] = []
        for document in self.documents:
            if isinstance(document, LandRegistrationDocument) and document.owner == valid_owner:
                land_doc_list.append(document)
        return land_doc_list

    def get_owner_building_documents(self, valid_owner: Owner) -> list[BuildingRegistrationDocument]:
        building_doc_list: list[BuildingRegistrationDocument] = []
        for document in self.documents:
            if isinstance(document, BuildingRegistrationDocument) and document.owner == valid_owner:
                building_doc_list.append(document)
        return building_doc_list

    def get_owner_documents(self, valid_owner: Owner) -> list[RegistrationDocument]:
        return self.get_owner_land_documents(valid_owner) + self.get_owner_building_documents(valid_owner)

    def get_owner_by_id(self, pass_id: str) -> Owner:
        for owner in self.registered_owners:
            if owner.passport_id == pass_id:
                return owner