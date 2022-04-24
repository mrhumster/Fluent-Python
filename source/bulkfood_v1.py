class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.wight = weight
        self.price = price

    def subtotal(self):
        return self.wight * self.price
