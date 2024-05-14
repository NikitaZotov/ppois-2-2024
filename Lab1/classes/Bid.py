class Bid:

    def __init__(self, bid):
        self.__bid = bid

    def get_bid(self):
        return self.__bid

    def set_bid(self, bid):
        try:
            self.__bid = int(bid)
        except ValueError:
            print("\033[31m" + "Ошибка: Ставка должна быть целым числом." + "\033[0m")