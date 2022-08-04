from box import *

i_user = User(user_id=430952068,
              name="Темний Лорд",
              username="heridium",
              phone_number="+380968793084",
              addres="Я за тобою 😁")
i_user.insert()

pizza = Group(name="Піца", prev_img="pizza.jpg")
pizza.insert()

g1 = get_group(pizza.group_id)

peperoni = Product(name="Пепероні",
                   prev_img="peperoni.png",
                   description="30см пепероні прямо з печі",
                   price=100,
                   group=g1)
peperoni.insert()

chease_pizza = Product(name="4 сира",
                       prev_img="4chease.jpg",
                       description="30см піца з неймовірним поєднанням 4 сирів",
                       price=120,
                       group=pizza)
chease_pizza.insert()

drink = Group(name="Напої", prev_img="drink.jpg")
drink.insert()

cola = Product(name="Кока-Кола",
               prev_img="cola.jpg",
               description="500мл кока-коли охолодженної в холодильнику",
               price=25,
               group=drink)
cola.insert()

juice = Product(name="Сік мультифрукт",
                prev_img="juice.jpg",
                description="Смачний та корисний сік котрий чудово доповнить смак піци",
                price=35,
                group=drink)
juice.insert()

sweet = Group(name="Солоденьке", prev_img="sweet.jpg")
sweet.insert()

donut = Product(name="Пончик",
                prev_img="donut.jpg",
                description="Солодкий пончик з ніжною кремовою начинкою",
                price=25,
                group=sweet)
donut.insert()

snikers = Product(name="Снікерс",
                  prev_img="snikers.jpg",
                  description="Солодкий батончик SNIKERS",
                  price=20,
                  group=sweet)
snikers.insert()
