from .clothes import Clothes
from .seller import Seller
from .customer import Customer


class Site:
    def __init__(self, name):
        self.__name: str = name
        self.__products: list[Clothes] = []
        self.__sellers: list[Seller] = []
        self.__customers: list[Customer] = []

    def get_name(self):
        return self.__name

    def get_products(self):
        return self.__products

    def get_sellers(self):
        return self.__sellers

    def get_customers(self):
        return self.__customers

    def add_product(self, clothes: Clothes):
        self.__products.append(clothes)

    def add_seller(self, seller: Seller):
        self.__sellers.append(seller)

    def add_customer(self, customer: Customer):
        self.__customers.append(customer)

    def search_clothes(self, category):
        match_products = []
        for product in self.__products:
            if product.get_category() == category:
                match_products.append(product)
        return match_products
