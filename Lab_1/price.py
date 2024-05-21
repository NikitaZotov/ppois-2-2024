class Price:
    def __init__(self, value):
        self.value = value

    def apply_discount(self, discount):
        self.value *= (1 - discount / 100)
