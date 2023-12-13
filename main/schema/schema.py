""" NOTE DO NOT EDIT & USE FUNCTION IN THIS FILE """
""" JUST FOR REFERENCES """

from sqlalchemy import MetaData, Table, Column, text, ForeignKey
# datatype only
from sqlalchemy import Integer, BigInteger, String, Boolean
from utils import call_engine


def drop_table(table):
    engine = call_engine()
    with engine.connect() as conn:
        for item in table:
            conn.execute(text(f"DROP TABLE IF EXISTS {item}"))
            print(f"DROPPED {item.upper()}")

def recreate_table_users(engine):
    metadata = MetaData()
    global users
    users = Table("users", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("email", String, unique=True, nullable=False),
        Column("phone", String),
        Column("password", String, nullable=False),
        Column("type_skin", String),
        Column("skin_problem", String),
        Column("images", String),    
        Column("token", String),
    )
    metadata.create_all(engine)

def recreate_table_foods(engine):
    metadata = MetaData()

    global foods
    foods = Table("foods", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id)),
        Column("name", String, nullable=False),
        Column("detail", String),           # same as description
        Column("images", String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
        Column("type_food", String),        # type food
    )
    metadata.create_all(engine)


def recreate_table_products(engine):
    metadata = MetaData()

    global products
    products = Table("products", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id)),
        Column("name", String, nullable=False),
        Column("detail", String),           # same as description
        Column("images", String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
        Column("type_product", String),        # type skincare
    )
    metadata.create_all(engine)