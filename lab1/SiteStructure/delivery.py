from .clothes import Clothes
import time

class Delivery:
    def __init__(self):
        self.__products: list[Clothes] = []

    def get_delivery(self):
        return self.__products

    def add_to_delivery(self, product):
        self.__products.append(product)

    def remove_delivery(self, product):
        self.__products.remove(product)

    def timer(self):
        start_time = time.time()
        current_time = time.time()
        while (current_time-start_time!=30):
            current_time = time.time()
            elapsed_time = current_time - start_time
            print(f"Elapsed time: {elapsed_time:.2f} seconds", end="\r")