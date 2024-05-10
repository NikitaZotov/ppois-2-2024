from ..model.entity.owner import Owner
from ..model.service.cadastral_agency import CadastralAgency
from ..validator.owner_validator import OwnerValidator
from ..view.menu import Menu


class OwnerController:
    def __init__(self):
        self._service = CadastralAgency()
        self._validator = OwnerValidator()

    def check_owner(self) -> Owner | None:

        def callback(_input):
            return _input

        passport_id = Menu.get_entry(callback, "Enter Passport ID: ")
        id_owners = dict([(i.passport_id, i) for i in self._service.registered_owners])
        if passport_id in id_owners:
            return id_owners[passport_id]
        else:
            while True:
                try:
                    if ((choice := Menu.get_entry(callback,
                                                  "You are not registered as an owner\nDo you want to register? Y/N\n"))
                            == "Y"):
                        return self.register_owner()
                    elif choice == "N":
                        return None
                    else:
                        raise ValueError("Invalid input!")
                except ValueError as e:
                    Menu.show_error(str(e))

    def register_owner(self) -> Owner:
        passport_id = Menu.get_entry(self._validator.validate_passport_id, "Enter passport ID: \n"
                                                                           "(The format fot passport ID is "
                                                                           "{7 digits}{1 uppercase letter}{3 d.}{2 "
                                                                           "up.l}{1 d.})\n")
        name = Menu.get_entry(self._validator.validate_name_or_surname, "Enter name: ")
        surname = Menu.get_entry(self._validator.validate_name_or_surname, "Enter surname: ")
        return self._service.register_owner(Owner(passport_id, name, surname))
