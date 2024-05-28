import random

from equipment import CoffeeMachine, CoffeeGrinder


class ShopPosition:
    def __init__(self, name: str, price: float, amount: float):
        self.name = name
        self.price = price
        self.amount = amount


class Shop:
    coffeeMachine: CoffeeMachine = CoffeeMachine(round(random.uniform(100, 200), 1))
    coffeeGrinder: CoffeeGrinder = CoffeeGrinder(round(random.uniform(50, 80), 1))
    milk: ShopPosition = ShopPosition('Milk', 5, 1)
    coffeeBeans: ShopPosition = ShopPosition('Coffee Beans', 30, 1)
