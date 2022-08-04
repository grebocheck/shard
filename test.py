from box import *
from users import User

new_user = User("Vadim", "+380968793084", "heridium", "Десь в Києві")

pizza_group = Group("PIZZA 30sm", "D:/pizzas.png")
drink_group = Group("Drink", "D:/drinks.png")

peperoni = Product("Peperoni 30sm", "D:/peperoni.png", "Peperoni pizza 30sm", 100, pizza_group)
gavayska = Product("Gavayska 30sm", "D:/gavayska.png", "Gavayska pizza 30sm", 100, pizza_group)
cola = Product("Coca-Cola", "D:/cola.png", "Coca-Cola 500ml bootle cooled", 20, drink_group)

obr_status = Status("Обробляється", "Ваше замовлення вже в обробці")

order = Order(new_user, [peperoni, gavayska, cola], [2, 1, 3], "fasted please", obr_status, True)

peperoni.change_price(85)

lis = order.list_products
for a in lis:
    print(a.price)