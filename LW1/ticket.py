class Ticket:
    def __init__(self):
        self.__cost: int = 0

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, cost: int):
        self.__cost: int = cost
