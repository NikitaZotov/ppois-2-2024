import random
from typing import List

import exceptions
import colors
import shop
from atmosphere import Atmosphere
from equipment import Equipment
from furniture import Table
from inventory import Inventory
from management import Management
from menu import Menu, Order
from people import Visitor, Barista


class CoffeeShop(Management, Atmosphere):
    def __init__(self, name: str, budget: float = 250.0) -> None:
        super(CoffeeShop, self).__init__(budget)
        Atmosphere.__init__(self)
        self.name: str = name

        self.__inventory: Inventory = Inventory()

        self.menu: Menu = Menu()

        barista: Barista = Barista()
        self.barista: Barista = barista
        self.visitor_list: List[Visitor] = []

        self.__order_list: List[Order] = []

        self.tables: List[Table] = []
        for i in range(0, 10):
            self.tables.append(Table())

    @property
    def order_list(self) -> List[str]:
        orders: List[str] = []
        for order in self.__order_list:
            order_str: str = ''
            for item in order.items:
                order_str += (str(item.name) + '\n')
            order_str += ('Total: ' + str(order.price) + '\n')
            orders.append(order_str)
        return orders

    def visitor_enter(self, visitor: Visitor) -> None:
        visitor.enter(self.atmosphere)
        self.visitor_list.append(visitor)
        for table in self.tables:  # free (or not) random table when new visitor enters
            if type(table.visitor) is Visitor:
                if not table.visitor.waiting:
                    if random.randint(0, 1) == 1:
                        table.free_table()

    def visitor_take_place(self, visitor: Visitor) -> None:
        for table in self.tables:
            if not table.is_taken:
                table.take_table(visitor)
                break

    def visitor_leave(self, visitor: Visitor) -> None:
        self.visitor_list.remove(visitor)

    def take_order(self) -> None:
        try:
            if len(self.visitor_list) == 0:
                raise exceptions.ListIsEmptyException
            else:
                for visitor in self.visitor_list:
                    if visitor.waiting:
                        order: Order = self.barista.take_order(visitor, self.menu)
                        self.__order_list.append(order)
                        self.income(order.price)
                        visitor.waiting = False
                        self.visitor_take_place(self.visitor_list[0])
                        break
                    elif visitor == self.visitor_list[len(self.visitor_list) - 1]:
                        raise exceptions.ListIsEmptyException
        except exceptions.ListIsEmptyException:
            print(colors.CRED + "There is no visitors in queue" + colors.CEND)

    def make_order(self) -> None:
        try:
            if len(self.__order_list) == 0:
                raise exceptions.ListIsEmptyException
            else:
                order: Order = self.__order_list[0]
                self.barista.make_order(self.inventory, self.__order_list)
                if len(order.items) == 0:
                    for visitor in self.visitor_list:
                        if visitor.order == order:
                            visitor.served = True
                            for table in self.tables:
                                if table.visitor == visitor:
                                    return
                            self.visitor_leave(visitor)
        except exceptions.ListIsEmptyException:
            print(colors.CRED + "There is no orders. Take an order first" + colors.CEND)

    @property
    def inventory(self) -> Inventory:
        return self.__inventory

    def create_atmosphere(self):
        self.switch_music()

    def buy_coffee_equipment(self, equipment: Equipment) -> None:
        try:
            if self.account >= equipment.price:
                self.expense(equipment.price)
                self.__inventory.coffee_equipment.append(equipment)
            else:
                raise exceptions.BudgetException
        except exceptions.BudgetException:
            print("Not enough money")

    def buy_atmosphere_equipment(self, name: str) -> None:
        pass

    def buy_storage_item(self, item: shop.ShopPosition) -> None:
        try:
            if self.account >= item.price:
                currentAmount: float = self.__inventory.storage.get(item.name.lower())
                self.expense(item.price)
                self.__inventory.storage.update({item.name.lower(): float(currentAmount) + item.amount})
            else:
                raise exceptions.BudgetException
        except exceptions.BudgetException:
            print("Not enough money")
