import contextlib

import bot_texts
from box import *

new_user = User(user_id=11111111111,
                name="TEST1",
                username="@test1",
                phone_number="+38090000000",
                addres="my hard drive")
new_user.insert()

pizza = Group(name="Pizza", prev_img="D:/group/img.png")
pizza.insert()

g1 = get_group(pizza.group_id)

peperoni = Product(name="Peperoni",
                   prev_img="D:/peperoni.png",
                   description="30sm peperoni",
                   price=100,
                   group=g1)
peperoni.insert()
print(peperoni.product_id)

chease_pizza = Product(name="Chease Pizza",
                       prev_img="D:/4_chease.png",
                       description="30sm 4 chease pizza",
                       price=120,
                       group=pizza)
chease_pizza.insert()
print(chease_pizza.product_id)

status_start = Status(name="START", description="Start worker")
status_start.insert()

my_order = Order(user=new_user,
                 list_products=[chease_pizza, peperoni],
                 list_amounts=[1, 2],
                 comment="Please hot",
                 status=status_start,
                 delivery=True)
my_order.insert()

he_order = get_order(1)
print(he_order.user.username)
print(he_order.delivery)
print(he_order.list_products[1].name)
print(he_order.list_amounts[1])

print(bot_texts.order_text(my_order))