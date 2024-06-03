from .Bid import Bid

class Lot:

    def __init__(self, name, stert_price = 0, bid = 0):
        self.__name = name
        self.__start_price = stert_price
        self.__bid = Bid(bid)

    @property
    def name(self):
        return self.__name

    @property
    def start_price(self):
        return self.__start_price

    @property
    def bid(self):
        return self.__bid.get_bid()

    @name.setter
    def name(self, name):
        try:
            if type(name) is not str:
                raise TypeError("\033[31m" + "Ошибка: Название лота должно быть строкой." + "\033[0m")
            else:
                self.__name = name
        except TypeError as ex:
            print(ex)

    @start_price.setter
    def start_price(self, price):
        try:
            self.__start_price = int(price)
        except ValueError:
            print( "\033[31m" + "Ошибка: Начальная цена должна быть целым числом." + "\033[0m")

    @bid.setter
    def bid(self, bid):
        self.__bid.set_bid(bid)
