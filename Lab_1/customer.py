from cart import Cart

class Customer:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.cart = Cart()

    def add_to_cart(self, seller, product_name, quantity):
        product = seller.find_product(product_name)
        if product:
            promotion = seller.find_promotion(product_name)
            if promotion:
                product_price = promotion.apply_discount(product.price)
            else:
                product_price = product.price

            total_price = product_price * quantity
            if total_price <= self.budget:
                self.cart.add_item(seller, product, quantity, product_price)
                #self.budget -= total_price


                print(f"{quantity} x {product.name} успешно добавлены в корзину.")
            else:
                print("Недостаточно средств для совершения покупки.")
        else:
            print(f"Продукт '{product_name}' не найден у продавца {seller.name}.")

    def purchase(self, seller):
        total_cost = self.cart.calculate_total()
        if total_cost <= self.budget:
            self.budget -= total_cost
            seller.account += total_cost  
            for item in self.cart.items:
                seller.products.remove(item['product'])  
            self.cart.clear()
            print(f"Покупка успешно совершена. Остаток бюджета: {self.budget:.2f}")
        else:
            print(f"Недостаточно средств для покупки. Требуемая сумма: {total_cost:.2f}, доступный бюджет: {self.budget:.2f}")
