from .seller import Seller


class ClothingCategory:
    def __init__(self):
        self.__category_list = {
            1: "shirts",
            2: "pants",
            3: "dresses",
            4: "accessories"
        }
        self.__category: str

    def set_category(self,num):
        self.__category = self.__category_list[num]

    def get_category(self):
        return self.__category

    def get_category_list(self):
        return self.__category_list

class Clothes:
    def __init__(self, name, price, category, seller):
        self.__name: str = name
        self.__price: int = price
        self.__category: str = category
        self.__seller: Seller = seller

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_category(self):
        return self.__category

    def get_seller(self):
        return self.__seller
