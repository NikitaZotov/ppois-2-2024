class Promotion:
    def __init__(self, product_name, discount_percent):
        self.product_name = product_name
        self.discount_percent = discount_percent

    def apply_discount(self, price):
        discount = price * (self.discount_percent / 100)
        return price - discount
