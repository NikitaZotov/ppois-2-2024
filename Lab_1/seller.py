from product import Product
import datetime
from promotion import Promotion

class Seller:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.account = 0.0
        self.promotions = []

    def add_product(self, product_name, price, expiration_date):
        expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
        current_date = datetime.date.today()

        if expiration_date < current_date:
            print(f"Невозможно добавить продукт '{product_name}', т.к. срок годности истек.")
            return

        product = Product(product_name, price, expiration_date)
        self.products.append(product)
        print(f"Товар '{product_name}' успешно добавлен.")

    def find_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                return product
        return None

    def show_products(self):
        if self.products:
            print(f"Товары продавца {self.name}:")
            for product in self.products:
                promotion = self.find_promotion(product.name)
                if promotion:
                    discounted_price = promotion.apply_discount(product.price)
                    print(f"{product.name} - {discounted_price:.2f} (скидка {promotion.discount_percent}%)")
                else:
                    print(f"{product.name} - {product.price:.2f}")
        else:
            print(f"У продавца {self.name} нет товаров.")

    def add_promotion(self, product_name, discount_percent):
        promotion = Promotion(product_name, discount_percent)
        self.promotions.append(promotion)
        print(f"Акция '{discount_percent}%' на товар '{product_name}' успешно добавлена.")

    def find_promotion(self, product_name):
        for promotion in self.promotions:
            if promotion.product_name == product_name:
                return promotion
        return None
