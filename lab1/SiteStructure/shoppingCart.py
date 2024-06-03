from .clothes import Clothes


class ShoppingCart:
    def __init__(self):
        self.__products: list[Clothes] = []

    def add_to_cart(self, product):
        self.__products.append(product)

    def remove_from_cart(self, product):
        self.__products.remove(product)

    def get_cart_list(self):
        return self.__products

    def get_total_price(self):
        return sum(product.get_price() for product in self.__products)