import unittest
from typing import List
from unittest import TestCase

from coffee_shop import CoffeeShop
from equipment import CoffeeMachine, CoffeeGrinder
from inventory import Inventory
from menu import Menu
from people import Visitor
from shop import ShopPosition


class TestCoffeeShop(unittest.TestCase):
    def setUp(self):
        self.coffee_shop: CoffeeShop = CoffeeShop('Name')
        self.visitor: Visitor = Visitor()
        self.menu: Menu = Menu()
        self.menu.default_menu()
        self.coffee_shop.menu = self.menu

    def test_coffee_shop_creation(self):
        self.assertEqual(self.coffee_shop.name, 'Name')
        self.assertEqual(self.coffee_shop.account, 250.0)
        self.assertEqual(self.coffee_shop.visitor_list, [])

    def test_visitor_enter(self):
        self.coffee_shop.visitor_enter(self.visitor)
        self.assertEqual(self.coffee_shop.visitor_list[0], self.visitor)

    def test_visitor_enter2(self):
        for i in range(0, 10):
            self.coffee_shop.visitor_enter(visitor=Visitor())
            self.coffee_shop.take_order()
            self.coffee_shop.make_order()
        self.coffee_shop.visitor_enter(self.visitor)

    def test_visitor_take_place(self):
        self.coffee_shop.visitor_take_place(self.visitor)
        is_taken: bool = False
        for table in self.coffee_shop.tables:
            if table.is_taken:
                is_taken = True
        self.assertEqual(is_taken, True)

    def test_visitor_leave(self):
        self.coffee_shop.visitor_enter(self.visitor)
        self.assertEqual(self.coffee_shop.visitor_list[0], self.visitor)
        self.coffee_shop.visitor_leave(self.visitor)
        self.assertEqual(len(self.coffee_shop.visitor_list), 0)

    def test_take_order(self):
        self.coffee_shop.take_order()
        self.assertEqual(len(self.coffee_shop.order_list), 0)
        self.coffee_shop.visitor_enter(self.visitor)
        self.coffee_shop.take_order()
        self.assertEqual(len(self.coffee_shop.order_list), 1)

    def test_order_list(self):
        self.coffee_shop.visitor_enter(self.visitor)
        self.coffee_shop.take_order()
        ls: List[str] = self.coffee_shop.order_list
        self.assertEqual(len(ls), 1)

    def test_make_order(self):
        self.assertEqual(len(self.coffee_shop.order_list), 0)
        self.coffee_shop.make_order()
        self.assertEqual(len(self.coffee_shop.order_list), 0)

    def test_create_atmosphere(self):
        self.coffee_shop.create_atmosphere()
        self.assertEqual(self.coffee_shop.music, True)

    def test_buy_coffee_equipment(self):
        self.coffee_shop.inventory.coffee_equipment.clear()
        machine: CoffeeMachine = CoffeeMachine(10000)
        machine2: CoffeeMachine = CoffeeMachine(100)
        self.coffee_shop.buy_coffee_equipment(machine)
        self.coffee_shop.buy_coffee_equipment(machine2)
        self.assertEqual(self.coffee_shop.inventory.coffee_equipment[0], machine2)

    def test_buy_storage_item(self):
        self.coffee_shop.expense(200)
        self.coffee_shop.buy_storage_item(ShopPosition('Milk', 50, 10))
        self.assertEqual(self.coffee_shop.inventory.storage.get('milk'), 10)
        self.coffee_shop.buy_storage_item(ShopPosition('Milk', 50, 10))
        self.assertEqual(self.coffee_shop.inventory.storage.get('milk'), 10)
