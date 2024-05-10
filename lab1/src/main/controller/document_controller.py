from src.main.model.entity.owner import Owner
from src.main.model.entity.registration_document import RegistrationDocument, LandRegistrationDocument, \
    BuildingRegistrationDocument
from src.main.model.service.cadastral_agency import CadastralAgency
from exception import BackException
from src.main.view.menu import Menu


class DocumentController:
    def __init__(self):
        self._service = CadastralAgency()

    def choose_land_plot_document(self, valid_owner: Owner, menu_context: str) -> LandRegistrationDocument:
        land_documents: list[LandRegistrationDocument] = self._service.get_owner_land_documents(valid_owner)
        if len(land_documents) == 0:
            raise ValueError("No land documents registered for this owner")
        land: LandRegistrationDocument | None = None

        def set_land(land_plot):
            nonlocal land
            land = land_plot

        Menu.print_menu(
            (
                menu_context
            ),
            {
                **{l.short_desc(): lambda: set_land(l) for l in land_documents},
                (0, "Back"): lambda: None,
            }
        )
        if not land:
            raise BackException()
        return land

    def choose_building_document(self, valid_owner: Owner, menu_context: str) -> BuildingRegistrationDocument:
        building_docs = self._service.get_owner_building_documents(valid_owner)
        if len(building_docs) == 0:
            raise ValueError("No building documents registered for this owner")
        document: BuildingRegistrationDocument | None = None

        def set_building_doc(build_doc):
            nonlocal document
            document = build_doc

        Menu.print_menu(
            (
                menu_context
            ),
            {
                **{b.short_desc(): (lambda b=b: set_building_doc(b)) for b in building_docs},
                (0, "Back"): lambda: None,
            }
        )
        if not document:
            raise BackException()
        return document

    def get_all_documents_of_owner(self, valid_owner: Owner) -> None:
        doc_list = self._service.get_owner_documents(valid_owner)
        if len(doc_list) == 0:
            raise ValueError("No documents registered for this owner")
        back_flag = False

        def back():
            nonlocal back_flag
            back_flag = True

        while not back_flag:
            Menu.print_menu(
                (
                    f"{valid_owner.first_name[0]}.{valid_owner.last_name}'s Documents"
                ),
                {
                    **{d.short_desc(): (lambda d=d: self.__show_full_document(d)) for d in doc_list},
                    (0, "Back"): lambda: back()
                }
            )

    def __show_full_document(self, doc: RegistrationDocument):
        choice: str = ""

        def callback(_input):
            nonlocal choice
            choice = _input

        Menu.get_entry(callback, str(doc)+"\nEnter 0 to update or anything to go back: ")
        if choice == '0':
            doc.update()
