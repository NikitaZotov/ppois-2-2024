class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, seller, product, quantity, price):
        item = {
            'seller': seller,
            'product': product,
            'quantity': quantity,
            'price': price
        }
        self.items.append(item)

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item['price'] * item['quantity']
        return total

    def clear(self):
        self.items.clear()
