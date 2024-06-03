class Seller:
    def __init__(self, name, wallet):
        self.__name: str = name
        self.__wallet: int = wallet

    def get_name(self):
        return self.__name

    def get_wallet(self):
        return self.__wallet

    def change_wallet(self, transfer):
        self.__wallet += transfer
