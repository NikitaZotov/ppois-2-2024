from src.main.model.entity.enum.region import Region

LAND_PLOT_NUMBER_LENGTH = 6


class CadastralNumber:

    def __init__(self, terr_unit_region: Region = Region.DEFAULT,
                 land_plot_number: int = 0):
        self.__terr_unit_region = terr_unit_region
        self.__terr_unit_code = terr_unit_region.value["terr_unit_num"]
        self.__cadastral_block_number = str(terr_unit_region.value["blocks"])
        self.__land_plot_number = self.__verify_land_plot_number(land_plot_number)

    @property
    def cadastral_block_number(self):
        return self.__cadastral_block_number

    @cadastral_block_number.setter
    def cadastral_block_number(self, number: int):
        if 0 <= number <= self.__terr_unit_region.value["blocks"]:
            self.__cadastral_block_number = str(number)
        else:
            raise ValueError(f'Invalid cadastral block number: {number}')

    @property
    def land_plot_number(self):
        return self.__land_plot_number

    @land_plot_number.setter
    def land_plot_number(self, number: str):
        self.__land_plot_number = number

    @property
    def terr_unit_code(self):
        return self.__terr_unit_code

    def __str__(self):
        block_num = self.cadastral_block_number if int(self.cadastral_block_number) > 10 \
            else "0" + self.cadastral_block_number
        return f"{self.terr_unit_code}{block_num}{self.land_plot_number}"

    def __eq__(self, other):
        return str(self) == str(other)

    @staticmethod
    def __verify_land_plot_number(number: int) -> str:
        num_length = len(str(number))
        str_num = str(number)
        if num_length < LAND_PLOT_NUMBER_LENGTH:
            str_num = str_num.join(["0"*(LAND_PLOT_NUMBER_LENGTH-num_length)]) + str_num
        elif number > 999999 or number < 0:
            raise ValueError(f'Invalid land plot number: {number}')
        return str_num
