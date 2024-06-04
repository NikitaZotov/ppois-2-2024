from .shoppingCart import ShoppingCart
from .delivery import Delivery

class Customer:
    def __init__(self, name, wallet):
        self.__name = name
        self.__wallet: int = wallet
        self.__cart = ShoppingCart()
        self.__delivery = Delivery()

    def get_name(self):
        return self.__name

    def get_wallet(self):
        return self.__wallet

    def get_cart(self):
        return self.__cart

    def get_delivery(self):
        return self.__delivery

    def change_wallet(self, transfer):
        self.__wallet += transfer
