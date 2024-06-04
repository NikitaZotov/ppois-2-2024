from customer import Customer
from seller import Seller

class Market:
    def __init__(self):
        self.customers = []
        self.sellers = []

    def add_customer(self, customer):
        self.customers.append(customer)
        print(f"Покупатель {customer.name.capitalize()} успешно добавлен.")

    def find_customer(self, name):
        for customer in self.customers:
            if customer.name == name:
                return customer
        return None

    def add_seller(self, seller):
        self.sellers.append(seller)
        print(f"Продавец {seller.name.capitalize()} успешно добавлен.")

    def find_seller(self, name):
        for seller in self.sellers:
            if seller.name == name:
                return seller
        return None

    def show_customers(self):
        if self.customers:
            print("Список покупателей:")
            for customer in self.customers:
                print(f"{customer.name.capitalize()} - Бюджет: {customer.budget:.2f}")
        else:
            print("Нет зарегистрированных покупателей.")

    def show_sellers(self):
        if self.sellers:
            print("Список продавцов:")
            for seller in self.sellers:
                print(f"{seller.name.capitalize()}")
        else:
            print("Нет зарегистрированных продавцов.")
