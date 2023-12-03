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


def recreate_table_banners(engine):
    metadata = MetaData()
    
    banners = Table("banners", metadata,
        Column("id", String(36), primary_key=True),
        Column("title", String, unique=True, nullable=False),
        Column("image", String, nullable=False)
    )
    metadata.create_all(engine)


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
        Column("token", String),
    )
    metadata.create_all(engine)


def recreate_table_categories(engine):
    metadata = MetaData()

    global categories
    categories = Table("categories", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("images", String),
        Column("is_deleted", Boolean, default=False)
    )
    metadata.create_all(engine)


def recreate_table_products(engine):
    metadata = MetaData()

    global products
    products = Table("products", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, nullable=False),
        Column("detail", String),           # same as description
        Column("category_id", ForeignKey(categories.c.id)),
        Column("images", String),    # ["/image/image1", "/image/image2"]
        Column("type", String),        # type skincare
    )
    metadata.create_all(engine)