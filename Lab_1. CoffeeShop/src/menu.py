from typing import List


class MenuItem:
    def __init__(self, name: str, price: float):
        self.name: str = name
        try:
            if price <= 0:
                price = 2
                raise ValueError("Invalid price")
        except ValueError as error:
            print(f"Exception: {error}")
            print(f"Defaults are used")
        self.price: float = price


class Coffee(MenuItem):
    def __init__(self, name: str, price: float, coffee: float, milk: float = 0):
        super().__init__(name, price)
        try:
            if coffee < 0.009 or coffee > 0.018:
                coffee = 0.009
                raise ValueError("Coffee must be between 0.009 and 0.018")
        except ValueError as error:
            print(f"Exception: {error}")
            coffee = 0.009
            print(f"Defaults are used")
        try:
            if milk < 0 or milk > 0.300:
                milk = 0
                raise ValueError("Milk must be between 0 and 0.300")
        except ValueError as error:
            print(f"Exception: {error}")
            milk = 0
            print(f"Defaults are used")
        self.milk: float = milk
        self.coffee: float = coffee


class Dessert(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)


class Menu:
    """Menu of the coffee shop"""

    def __init__(self):
        self.coffee_menu: List[Coffee] = []
        self.dessert_menu: List[Dessert] = []

    def add_item(self, item: MenuItem) -> None:
        if type(item) is Coffee:
            self.coffee_menu.append(item)
        if type(item) is Dessert:
            self.dessert_menu.append(item)

    def default_menu(self) -> None:
        self.add_item(Coffee("espresso", 4, 0.009))
        self.add_item(Coffee("americano", 5, 0.009))
        self.add_item(Coffee("cappuccino", 5.5, 0.009, 0.180))
        self.add_item(Coffee("double cappuccino", 6.5, 0.018, 0.220))
        self.add_item(Coffee("latte", 6.0, 0.009, 0.220))

        self.add_item(Dessert("dessert", 4))


class Order:
    def __init__(self):
        self.items: List[MenuItem] = []
        self.price: float = 0

    def add_item(self, item: MenuItem):
        self.items.append(item)
        self.price += item.price
