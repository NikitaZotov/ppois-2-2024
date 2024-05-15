import random
from typing import List
from random import randint, choice

import colors
import inventory
import equipment
import menu
# from inventory import Inventory
from menu import Order, Menu


# from exceptions import ItemNotExistException


class Visitor:
    """Visitor of the coffee shop"""

    def __init__(self):
        self.__waiting: bool = True
        self.__served: bool = False
        self.__atmosphere: int = 0
        self.order: Order = Order()

    @property
    def waiting(self):
        return self.__waiting

    @waiting.setter
    def waiting(self, value: bool = False):
        self.__waiting = value

    @property
    def served(self):
        return self.__served

    @served.setter
    def served(self, value: bool = True):
        self.__served = value

    def enter(self, coffee_shop_atmosphere: float = 0.0) -> None:
        self.__atmosphere = coffee_shop_atmosphere

    def make_order(self, menu: Menu) -> Order:
        self.order = self.__randomize_order(menu)
        return self.order

    def __randomize_order(self, menu: Menu) -> Order:
        order: Order = Order()
        for i in range(0, randint(1, randint(2, 4))):
            if randint(0, 1) == 0:
                order.add_item(choice(menu.coffee_menu))
            else:
                order.add_item(choice(menu.dessert_menu))
        return order

    def pay(self) -> float:
        return self.order.price + self.__tip()

    def __tip(self) -> float:
        return self.order.price + self.order.price * random.uniform(1.0, self.__atmosphere)


class Barista:
    """Barista in the coffee shop"""

    def __init__(self):
        self.orders: List[Order] = []

    def take_order(self, visitor: Visitor, coffee_shop_menu: Menu) -> Order:
        """Gives visitor a menu and takes money from visitor"""
        order: Order = visitor.make_order(coffee_shop_menu)
        self.orders.append(order)
        visitor.pay()
        return order

    def make_order(self, inventory: inventory.Inventory, order: Order) -> None:
        coffee_positions: List[menu.Coffee] = []
        dessert_positions: List[menu.Dessert] = []
        for position in order.items:
            if type(position) is menu.Coffee:
                coffee_positions.append(position)
            if type(position) is menu.Dessert:
                dessert_positions.append(position)

        order.items = (self.__make_coffee(inventory, coffee_positions) +
                       self.__make_dessert(inventory, dessert_positions))

    def __make_coffee(self, inventory: inventory.Inventory, coffee_list: List[menu.Coffee]) -> List[menu.Coffee]:
        milk_amount: float = 0
        coffee_amount: float = 0
        try:
            for coffee in coffee_list:
                milk_amount += coffee.milk
                coffee_amount += coffee.coffee
            if milk_amount > inventory.storage.get("milk"):
                raise ValueError("Not enough milk to make coffee")
            if coffee_amount > inventory.storage.get("coffee beans"):
                raise ValueError("Not enough coffee beans to make coffee")
            while len(coffee_list) != 0:
                coffee: menu.Coffee = coffee_list.pop(0)
                current_coffee: float = inventory.storage.get("coffee beans")
                current_milk: float = inventory.storage.get("milk")
                for equip in inventory.coffee_equipment:
                    if type(equip) is equipment.CoffeeGrinder:
                        equip.use()
                    if type(equip) is equipment.CoffeeMachine:
                        equip.use()
                inventory.storage.update({"milk": current_milk - coffee.milk})
                inventory.storage.update({"coffee beans": current_coffee - coffee.coffee})
            return coffee_list
        except ValueError as err:
            print(colors.CRED, "Making coffee failed.", err, colors.CEND)
            return coffee_list

    def __make_dessert(self, inventory: inventory.Inventory, dessert_list: List[menu.Dessert]) -> List[menu.Dessert]:
        while len(dessert_list) != 0:
            dessert_list.pop(0)
        return dessert_list
