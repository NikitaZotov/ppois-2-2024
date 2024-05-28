from typing import List

from equipment import Equipment


class Inventory:
    coffee_equipment: List[Equipment] = []
    atmosphere_equipment: List[Equipment] = []

    storage: dict = {"coffee beans": 0,
                     "milk": 0}
