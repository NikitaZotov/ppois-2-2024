from typing import List
from unittest import TestCase

import exceptions
import menu
import people
from equipment import CoffeeMachine, CoffeeGrinder
from inventory import Inventory
from people import Visitor, Barista
from menu import Menu


class TestVisitor(TestCase):
    def setUp(self):
        self.visitor = Visitor()

    def test_waiting_getter(self):
        self.assertEqual(self.visitor.waiting, True)

    def test_waiting_setter(self):
        self.visitor.waiting = False
        self.assertEqual(self.visitor.waiting, False)

    def test_served_getter(self):
        self.assertEqual(self.visitor.served, False)

    def test_served_setter(self):
        self.visitor.served = True
        self.assertEqual(self.visitor.served, True)

    def test_enter(self):
        self.visitor.enter(1)

    def test_make_order(self):
        menu: Menu = Menu()
        menu.default_menu()
        self.visitor.make_order(menu)
        self.assertGreaterEqual(len(self.visitor.order.items), 1)

    def test_pay(self):
        self.visitor.pay()

    def test_pay_with_tip(self):
        menu: Menu = Menu()
        menu.default_menu()
        self.visitor.make_order(menu)
        self.assertGreater(self.visitor.pay(), self.visitor.order.price)


class TestBarista(TestCase):
    def setUp(self):
        self.barista: Barista = Barista()
        self.inventory: Inventory = Inventory()
        self.inventory.coffee_equipment.append(CoffeeMachine(0))
        self.inventory.coffee_equipment.append(CoffeeGrinder(0))
        self.inventory.storage['milk'] = 100
        self.inventory.storage['coffee beans'] = 100
        self.visitor: Visitor = Visitor()
        self.menu: Menu = Menu()
        self.menu.default_menu()

    def test_take_order(self):
        self.barista.take_order(self.visitor, self.menu)
        self.assertEqual(self.barista.take_order(self.visitor, self.menu), self.visitor.order)
        self.assertNotEqual(len(self.visitor.order.items), 0)

    def test_make_order(self):
        order: menu.Order = self.barista.take_order(self.visitor, self.menu)
        order_list: List[menu.Order] = [order]
        self.barista.make_order(self.inventory, order_list)
        self.assertEqual(len(order.items), 0)

    def test_make_order_with_no_milk(self):
        self.inventory.storage['milk'] = 0
        order: menu.Order = menu.Order()
        order.add_item(menu.Coffee('coffee', 1, 0.009, 0.100))
        order_list: List[menu.Order] = [order]
        self.barista.make_order(self.inventory, order_list)
        self.assertEqual(len(order.items), 1)

    def test_make_order_with_no_coffee(self):
        self.inventory.storage['coffee beans'] = 0
        self.inventory.storage['milk'] = 100
        order: menu.Order = menu.Order()
        order.add_item(menu.Coffee('coffee', 1, 0.009, 0.100))
        order_list: List[menu.Order] = [order]
        self.barista.make_order(self.inventory, order_list)
        self.assertEqual(len(order.items), 1)
