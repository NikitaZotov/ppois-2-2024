class Equipment:
    def __init__(self, price):
        self._price: float = price

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    def use(self):
        pass


class CoffeeMachine(Equipment):
    def __init__(self, price: float):
        super().__init__(price)


class CoffeeGrinder(Equipment):
    def __init__(self, price: float):
        super().__init__(price)
