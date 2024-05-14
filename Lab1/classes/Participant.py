class Participant:

    def __init__(self, number, name, money = 0):
        self.__number = number
        self.__name = name
        self.__money = money

    @property
    def number(self):
        return self.__number

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        try:
            if type(name) is not str:
                raise TypeError("\033[31m" + "Ошибка: Имя участника должно быть строкой." + "\033[0m")
            else:
                self.__name = name
        except TypeError as ex:
            print(ex)

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, money):
        try:
            self.__money = int(money)
        except ValueError:
            print("\033[31m" + "Ошибка: Сумма денег должна быть числом." + "\033[0m")


    def raise_price(self, price, bid):
        if price + bid <= self.money:
            return price + bid
        else:
            print("\033[31m" + "Данный участник не может повысить цену на данный лот." + "\033[0m")
            return price

    def pay_money(self, cost):
        self.__money = self.__money - cost