from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select

import bot_texts
import db
import settings
from loge import log

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

product = db.product
group = db.group
order = db.order
user = db.user
banlist = db.banlist


# імпорт користувача з бази данних по user_id
def get_user(user_id):
    log(f"викликано get_user {user_id}")
    s = select([user]).where(user.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_user = User(user_id=row[0], name=row[1], username=row[2], phone_number=row[3], addres=row[4])
    return l_user


# перевірка чи є користувач в базі данних
def extend_user(user_id):
    log(f"викликано extend_user {user_id}")
    s = select([user]).where(user.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return True
    else:
        return False


# імпорт продукту з бази данних по user_id
def get_product(product_id):
    log(f"викликано get_product {product_id}")
    s = select([product]).where(product.c.product_id == product_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_product = Product(product_id=row[0],
                        name=row[1],
                        prev_img=row[2],
                        description=row[3],
                        price=row[4],
                        group=get_group(row[5]))
    return l_product


# пошук продукта по його назві
def get_product_by_name(product_name):
    log(f"викликано get_product_by_name {product_name}")
    s = select([product]).where(product.c.name == product_name)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_product = Product(product_id=row[0],
                        name=row[1],
                        prev_img=row[2],
                        description=row[3],
                        price=row[4],
                        group=get_group(row[5]))
    return l_product


# перевірка чи є продукт в базі данних
def extend_product(name):
    log(f"викликано extend_product {name}")
    s = select([product]).where(product.c.name == name)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


# Перевірка на можливість конвертації
def extend_int(text):
    log(f"викликано extend_int {text}")
    try:
        int(text)
        return True
    except:
        return False


# імпорт групи продуктів з бази данних по user_id
def get_group(group_id):
    log(f"викликано get_group {group_id}")
    s = select([group]).where(group.c.group_id == group_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_group = Group(group_id=row[0], name=row[1], prev_img=row[2])
    return l_group


# пошук ID групи по відомому NAME
def get_group_id(group_name):
    log(f"викликано get_group_id {group_name}")
    s = select([group]).where(group.c.name == group_name)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    return row[0]


# пошук всіх продуктів по ID їх групи
def get_products_by_group(group_id):
    log(f"викликано get_products_by_group {group_id}")
    mass = []
    get = product.select().where(product.c.group == group_id)
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        mass.append(Product(product_id=row[0],
                            name=row[1],
                            prev_img=row[2],
                            description=row[3],
                            price=row[4],
                            group=get_group(row[5])))
    return mass


# Вибірка всіх груп з бази данних
def select_all_group():
    log(f"викликано select_all_group")
    mass = []
    get = group.select()
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        mass.append(Group(group_id=row[0], name=row[1], prev_img=row[2]))
    return mass


# перевірка чи є група в базі данних
def extend_group(name):
    log(f"викликано extend_group {name}")
    s = select([group]).where(group.c.name == name)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


# імпорт замовлення з бази данних по user_id
def get_order(order_id):
    log(f"викликано get_order {order_id}")
    s = select([order]).where(order.c.order_id == order_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()

    l_order = Order(order_id=row[0],
                    user=get_user(row[1]),
                    content=row[2],
                    status=get_status(row[3]),
                    create_date=row[4],
                    close_date=row[5])
    return l_order


#  Пошук всіх активних замовлень для даного користувача
def get_my_open_orders(user_id):
    log(f"викликано get_my_open_orders {user_id}")
    orders = []
    s = select([order]).where(order.c.user == user_id).where(order.c.close_date == bot_texts.none_close_date)
    conn = engine.connect()
    result = conn.execute(s)
    for row in result:
        l_order = Order(order_id=row[0],
                        user=get_user(row[1]),
                        content=row[2],
                        status=get_status(row[3]),
                        create_date=row[4],
                        close_date=row[5])
        orders.append(l_order)
    return orders


#  Пошук всіх активних замовлень
def get_all_open_orders():
    log(f"викликано get_all_open_orders")
    orders = []
    s = select([order]).where(order.c.close_date == bot_texts.none_close_date)
    conn = engine.connect()
    result = conn.execute(s)
    for row in result:
        l_order = Order(order_id=row[0],
                        user=get_user(row[1]),
                        content=row[2],
                        status=get_status(row[3]),
                        create_date=row[4],
                        close_date=row[5])
        orders.append(l_order)
    return orders


# підрахунок ціни замовлення
def get_price(list_products, list_amounts, delivery):
    log(f"викликано get_price {list_products}, {list_amounts}, {delivery}")
    prices = 0
    for a in range(len(list_products)):
        prices += list_products[a].price * list_amounts[a]
    if delivery != bot_texts.none_addres:
        prices += settings.DELIVERY_PRICE
    return prices


def extend_banlist(user_id):
    log(f"викликано extend_banlist {user_id}")
    s = select([banlist]).where(banlist.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return True
    else:
        return False


def db_ban(user_id):
    log(f"викликано db_ban {user_id}")
    if extend_banlist(user_id):
        if settings.DEBUG:
            log(f"Поповнення бан листу {user_id}")
        ins = banlist.insert().values(user_id=user_id)
        conn = engine.connect()
        result = conn.execute(ins)
        if settings.DEBUG:
            print(result)
        dele = delete(order).where(order.c.user == user_id)
        conn = engine.connect()
        result = conn.execute(dele)
        if settings.DEBUG:
            print(result)
        ret = bot_texts.ban_succes
    else:
        ret = bot_texts.ban_unsucces
    return ret


def db_unban(user_id):
    log(f"викликано db_unban {user_id}")
    if not extend_banlist(user_id):
        if settings.DEBUG:
            log(f"Поповнення бан листу {user_id}")
        ins = delete(banlist).where(banlist.c.user_id == user_id)
        conn = engine.connect()
        result = conn.execute(ins)
        if settings.DEBUG:
            print(result)
        ret = bot_texts.unban_succes
    else:
        ret = bot_texts.unban_unsucces
    return ret


# клас описуючий користувача
class User:
    def __init__(self, user_id, name, username, phone_number, addres):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.phone_number = phone_number
        self.addres = addres
        log(f"Ініційовано User {[self.user_id]}")

    # запис користувача в базу данних
    def insert(self):
        ins = user.insert().values(user_id=self.user_id,
                                   name=self.name,
                                   username=self.username,
                                   phone=self.phone_number,
                                   addres=self.addres)
        conn = engine.connect()
        result = conn.execute(ins)
        print(result)
        log(f"Записано User {[self.user_id]}")

    # оновлення даних для бази данних
    def update(self):
        upd = update(user).where(user.c.user_id == self.user_id).values(user_id=self.user_id,
                                                                        name=self.name,
                                                                        username=self.username,
                                                                        phone=self.phone_number,
                                                                        addres=self.addres)
        conn = engine.connect()
        result = conn.execute(upd)
        print(result)
        log(f"Оновлено User {[self.user_id]}")


# клас описуючий продукт
class Product:
    def __init__(self, name, prev_img, description, price, group, product_id=None):
        self.product_id = product_id
        self.name = name
        self.prev_img = prev_img
        self.description = description
        self.price = price
        self.group = group
        log(f"Ініційовано Product {[self.product_id, self.name, self.prev_img, self.description, self.price, self.group.name]}")

    # запис продукту в базу данних
    def insert(self):
        ins = product.insert().values(name=self.name,
                                      prev_img=self.prev_img,
                                      description=self.description,
                                      price=self.price,
                                      group=self.group.group_id)
        conn = engine.connect()
        result = conn.execute(ins)
        self.product_id = result.lastrowid
        print(result)
        log(f"Записано Product {[self.product_id, self.name, self.prev_img, self.description, self.price, self.group.name]}")

    # видалення даних з бази данних
    def delete(self):
        dele = delete(product).where(product.c.product_id == self.product_id)
        conn = engine.connect()
        result = conn.execute(dele)
        print(result)
        log(f"Видалено Product {[self.product_id, self.name, self.prev_img, self.description, self.price, self.group.name]}")

    # оновлення даних для бази данних
    def update(self):
        upd = update(product).where(product.c.product_id == self.product_id).values(product_id=self.product_id,
                                                                                    name=self.name,
                                                                                    prev_img=self.prev_img,
                                                                                    description=self.description,
                                                                                    price=self.price,
                                                                                    group=self.group.group_id)
        conn = engine.connect()
        result = conn.execute(upd)
        print(result)
        log(f"Оновлено Product {[self.product_id, self.name, self.prev_img, self.description, self.price, self.group.name]}")


# клас описуючий групу товарів
class Group:
    def __init__(self, name, prev_img, group_id=None):
        self.group_id = group_id
        self.name = name
        self.prev_img = prev_img
        log(f"Ініційовано Group {[self.group_id, self.name, self.prev_img]}")

    # запис групи продуктів в базу данних
    def insert(self):
        if settings.DEBUG:
            log("Використано функцію запису в БД")
        ins = group.insert().values(name=self.name,
                                    prev_img=self.prev_img,
                                    )
        conn = engine.connect()
        result = conn.execute(ins)
        self.group_id = result.lastrowid
        print(result)
        log(f"Записано Group {[self.group_id, self.name, self.prev_img]}")

    # оновлення даних для бази данних
    def update(self):
        upd = update(group).where(group.c.group_id == self.group_id).values(group_id=self.group_id,
                                                                            name=self.name,
                                                                            prev_img=self.prev_img)
        conn = engine.connect()
        result = conn.execute(upd)
        print(result)
        log(f"Оновлено Group {[self.group_id, self.name, self.prev_img]}")

    # видалення даних з бази данних
    def delete(self):
        products = get_products_by_group(self.group_id)
        for b in products:
            b.delete()
        dele = delete(group).where(group.c.group_id == self.group_id)
        conn = engine.connect()
        result = conn.execute(dele)
        print(result)
        log(f"Видалено Group {[self.group_id, self.name, self.prev_img]}")


# клас описуючий замовлення
class Order:
    def __init__(self, user, status, content, create_date, close_date, order_id=None):
        self.order_id = order_id
        self.user = user
        self.content = content
        self.status = status
        self.create_date = create_date
        self.close_date = close_date
        log(f"Ініційовано Order {[self.order_id, self.user.user_id]}")

    # запис замовлення в базу данних
    def insert(self):
        if settings.DEBUG:
            log("Використано функцію запису в БД")

        ins = order.insert().values(user=self.user.user_id,
                                    content=self.content,
                                    status=self.status.status_id,
                                    create_date=self.create_date,
                                    close_date=self.close_date)
        conn = engine.connect()
        result = conn.execute(ins)
        self.order_id = result.lastrowid
        print(result)
        log(f"Записано Order {[self.order_id, self.user.user_id]}")

    # оновлення даних для бази данних
    def update(self):
        upd = update(order).where(order.c.order_id == self.order_id).values(order_id=self.order_id,
                                                                            user=self.user.user_id,
                                                                            content=self.content,
                                                                            status=self.status.status_id,
                                                                            create_date=self.create_date,
                                                                            close_date=self.close_date)
        conn = engine.connect()
        result = conn.execute(upd)
        print(result)
        log(f"Оновлено Order {[self.order_id, self.user.user_id]}")


# клас статусу замовлення
class Status:
    def __init__(self, status_id, name, description):
        self.status_id = status_id
        self.name = name
        self.description = description


status_start = Status(status_id=1, name=bot_texts.status_start_name,
                      description=bot_texts.status_start_description)  # id 1

status_close = Status(status_id=2, name=bot_texts.status_close_name,
                      description=bot_texts.status_close_description)  # id 2

status_work = Status(status_id=3, name=bot_texts.status_work_name,
                     description=bot_texts.status_work_description)  # id 3

status_delivery = Status(status_id=4, name=bot_texts.status_delivery_name,
                         description=bot_texts.status_delivery_description)  # id 4

status_complete = Status(status_id=5, name=bot_texts.status_complete_name,
                         description=bot_texts.status_complete_description)  # id 5


# імпорт статусу по його ID
def get_status(status_id):
    mass = get_all_status()
    l_status = mass[0]
    for a in mass:
        if status_id == a.status_id:
            l_status = a
    return l_status


# імпорт всіх статусів
def get_all_status():
    mass = [status_start, status_close, status_work, status_delivery, status_complete]
    return mass
