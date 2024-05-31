from cad_agency.model.entity.cadastral_number import CadastralNumber
from cad_agency.model import CadastralAgency


class LandPlotValidator:
    def __init__(self):
        self._service = CadastralAgency()

    def validate_coordinates(self, str_coordinates: str) -> tuple[float, float]:
        coordinates = tuple(map(float, str_coordinates.replace(" ", "").split(',')))
        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1])
            if coordinates not in [i.coordinates for i in self._service.registered_land_plots]:
                return coordinates
        else:
            raise ValueError(f'Invalid coordinates or they are already used')

    def validate_area(self, area: str) -> float:
        try:
            area = float(area)
        except ValueError as e:
            raise ValueError(f'Invalid area: {e}')
        if area < 0:
            raise ValueError(f'Invalid area: must be positive')
        return area

    def validate_cadastral_number(self, cad_number: CadastralNumber, cad_block_num: int) -> str:
        cad_number.cadastral_block_number = cad_block_num
        cad_number = str(cad_number)
        if cad_number not in [i.cadastral_number for i in self._service.registered_land_plots]:
            return cad_number
        else:
            raise ValueError("This number already exists")
