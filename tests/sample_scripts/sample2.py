inventory = {"apples": 10, "bananas": 5}

item = "apples"
quantity_sold = 3

if item in inventory:
    inventory[item] = inventory[item] - quantity_sold

total_items = 0
for key in inventory:
    total_items += inventory[key]

print("Total items left:", total_items)


class ShoppingCart:
    def __init__(self):
        self.total = 0

    def add_item(self, price):
        self.total += price
        return self.total


cart = ShoppingCart()
cart.total = 0
final_total = cart.add_item(50)

print("Cart total:", final_total)