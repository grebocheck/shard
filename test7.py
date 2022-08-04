from box import *
from datetime import datetime

p1 = get_product(1)
p2 = get_product(2)
p3 = get_product(3)

list_products = [get_product(1), get_product(3), get_product(4)]
list_amounts = [1, 3, 4]

comment = bot_texts.non_comment

it_user = get_user(430952068)
it_order_content = bot_texts.order_content(list_products=list_products,
                                           list_amounts=list_amounts,
                                           delivery=it_user.addres,
                                           comment=comment)

my_order = Order(user=it_user,
                 content=it_order_content,
                 status=get_status(1),
                 create_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                 close_date=bot_texts.none_close_date, )
my_order.insert()
my_order.status = status_complete
my_order.update()

he_order = get_order(my_order.order_id)
print(he_order.status.name)