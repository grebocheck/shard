from box import *

pizza = Group(name="Pizza", prev_img="D:/group/img.png")
pizza.insert()

g1 = get_group(pizza.group.group_id)

peperoni = Product("Peperoni", "D:/peperoni.png", "30sm peperoni", 100, g1)
peperoni.insert()

my_pizza = get_product(peperoni.product_id)
print(my_pizza.group.name)