from cad_agency.model import CadastralAgency
import re


class OwnerValidator:
    def __init__(self):
        self._service = CadastralAgency()

    def validate_passport_id(self, passport_id: str) -> str:
        pattern = re.compile('^\d{7}[A-Z]\d{3}[A-Z]{2}\d$')
        if pattern.match(passport_id) and passport_id not in [i.passport_id for i in self._service.registered_owners]:
            return passport_id
        else:
            raise ValueError('Passport ID is not valid or already exists!')

    def validate_name_or_surname(self, name_or_surname: str) -> str:
        pattern = re.compile('^[A-Z][a-z]*$')
        if pattern.match(name_or_surname):
            return name_or_surname
        else:
            raise ValueError('Name or surname is not valid')
