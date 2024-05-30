import enum


class Region(enum.Enum):
    DEFAULT = {
        "terr_unit_num": "0000000000",
        "blocks": 0
    }
    GRODNO = {
        "terr_unit_num": "4401000000",
        "blocks": 2
    }
    MINSK = {
        "terr_unit_num": "5000000000",
        "blocks": 9
    }
    MINSK_RG = {
        "terr_unit_num": "6000000000",
        "blocks": 22
    }
    GOMEL = {
        "terr_unit_num": "3401000000",
        "blocks": 4
    }
    VITEBSK = {
        "terr_unit_num": "2401000000",
        "blocks": 3
    }
    MOGILEV = {
        "terr_unit_num": "7401000000",
        "blocks": 4
    }
    BREST = {
        "terr_unit_num": "1401000000",
        "blocks": 6
    }

    def __eq__(self, other):
        return self.value["terr_unit_num"] == other.value["terr_unit_num"]
