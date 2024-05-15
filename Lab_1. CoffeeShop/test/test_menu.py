from typing import List
from unittest import TestCase

from menu import Coffee, MenuItem, Dessert, Order, Menu


class TestMenu(TestCase):
    def setUp(self):
        self.menu: Menu = Menu()

    def test_add_item(self):
        coffee: Coffee = Coffee('coffee', 5, 0.009, 0.1)
        dessert: Dessert = Dessert('dessert', 2)
        self.menu.add_item(coffee)
        self.assertListEqual(self.menu.coffee_menu, [coffee])
        self.assertListEqual(self.menu.dessert_menu, [])
        self.menu.add_item(dessert)
        self.assertListEqual(self.menu.coffee_menu, [coffee])
        self.assertListEqual(self.menu.dessert_menu, [dessert])

    def test_default_menu(self):
        self.menu.default_menu()
        self.assertEqual(len(self.menu.coffee_menu), 5)
        self.assertEqual(len(self.menu.dessert_menu), 1)


class TestOrder(TestCase):
    def setUp(self):
        self.order: Order = Order()

    def test_add_item(self):
        self.assertEqual(len(self.order.items), 0)
        self.assertEqual(self.order.price, 0)
        coffee: Coffee = Coffee('coffee', 5, 0.009, 0.1)
        dessert: Dessert = Dessert('dessert', 2)
        self.order.add_item(coffee)
        self.order.add_item(dessert)
        self.assertListEqual(self.order.items, [coffee, dessert])
        self.assertEqual(self.order.price, 7)


class TestMenuItem(TestCase):
    def test_normal_init(self):
        item: MenuItem = MenuItem("item", 10)
        self.assertEqual(item.name, 'item')
        self.assertEqual(item.price, 10)

    def test_wrong_price_init(self):
        item: MenuItem = MenuItem("item", -1)
        self.assertEqual(item.name, 'item')
        self.assertEqual(item.price, 2)


class TestCoffee(TestCase):
    def test_normal_init(self):
        coffee: Coffee = Coffee('coffee', 5, 0.009, 0.1)
        self.assertEqual(coffee.name, 'coffee')
        self.assertEqual(coffee.price, 5)
        self.assertEqual(coffee.coffee, 0.009)
        self.assertEqual(coffee.milk, 0.1)

    def test_all_exceptions_init(self):
        coffee: Coffee = Coffee('coffee', 0, 0, 100)
        self.assertEqual(coffee.name, 'coffee')
        self.assertEqual(coffee.price, 2)
        self.assertEqual(coffee.coffee, 0.009)
        self.assertEqual(coffee.milk, 0)

    def test_wrong_milk_exception_init(self):
        coffee: Coffee = Coffee('coffee', 1, 0.009, 100)
        self.assertEqual(coffee.name, 'coffee')
        self.assertEqual(coffee.price, 1)
        self.assertEqual(coffee.coffee, 0.009)
        self.assertEqual(coffee.milk, 0)

    def test_wrong_coffee_exception_init(self):
        coffee: Coffee = Coffee('coffee', 1, 0, 0.100)
        self.assertEqual(coffee.name, 'coffee')
        self.assertEqual(coffee.price, 1)
        self.assertEqual(coffee.coffee, 0.009)
        self.assertEqual(coffee.milk, 0.1)


class TestDessert(TestCase):
    def test_init(self):
        dessert: Dessert = Dessert('dessert', 2)
