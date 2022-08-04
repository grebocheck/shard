from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from loge import log

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

user = Table(
    'user', meta,
    Column('user_id', Integer, primary_key=True),
    Column('name', String),
    Column('username', String),
    Column('phone', String),
    Column('addres', String),
)

product = Table(
    'product', meta,
    Column('product_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('prev_img', String),
    Column('description', String),
    Column('price', Integer),
    Column('group', String),
)

group = Table(
    'group', meta,
    Column('group_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('prev_img', String),
)

order = Table(
    'order', meta,
    Column('order_id', Integer, primary_key=True, autoincrement=True),
    Column('user', Integer),
    Column('content', String),
    Column('status', Integer),
    Column('create_date', String),
    Column('close_date', String),
)

banlist = Table(
    'banlist', meta,
    Column('user_id', Integer, primary_key=True),
)

if __name__ == '__main__':
    meta.create_all(engine)
    log("Запущено db.py в режимі main")
