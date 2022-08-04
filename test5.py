import contextlib
from box import *

pizza = Group(name="Pizza", prev_img="D:/group/img.png")
pizza.insert()

g1 = get_group(pizza.group_id)

peperoni = Product(name="Peperoni", prev_img="D:/peperoni.png", description="30sm peperoni", price=100, group=g1)
peperoni.insert()

my_pizza = get_product(peperoni.product_id)
print(my_pizza.group.name)
print(my_pizza.group.group_id)
print(my_pizza.product_id)
