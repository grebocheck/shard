from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import random
import settings
from sqlalchemy.sql import select
import db
from loge import log

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

user = db.user


# імпорт користувача з бази данних по user_id
def get_user(user_id):
    if settings.DEBUG:
        log(f"Завантажено користувача {user_id}")
    s = select([user]).where(user.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_user = User(user_id=row[0], name=row[1], username=row[2], phone_number=row[3], addres=row[4])
    return l_user


# клас описуючий користувача
class User:
    def __init__(self, user_id, name, username, phone_number, addres):
        if settings.DEBUG:
            log(f"Ініційовано користувача {[user_id, name, username, phone_number, addres]}")
        self.user_id = user_id
        self.name = name
        self.username = username
        self.phone_number = phone_number
        self.addres = addres

    # запис користувача в базу данних
    def insert(self):
        if settings.DEBUG:
            log("Використано функцію запису в БД")
        ins = user.insert().values(user_id=self.user_id,
                                   name=self.name,
                                   username=self.username,
                                   phone=self.phone_number,
                                   addres=self.addres)
        conn = engine.connect()
        result = conn.execute(ins)
        if settings.DEBUG:
            print(result)
