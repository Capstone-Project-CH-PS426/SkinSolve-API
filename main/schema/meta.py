#!/usr/bin/env python3
#-*- coding: utf-8 -*-


from utils import call_engine, call_local_engine
from sqlalchemy import MetaData, Table, Column, String, Boolean, ForeignKey, Integer, BigInteger, text

def db_init():

    engine = call_engine()
    # engine = call_local_engine()

    metadata = MetaData()

    banners = Table("banners", metadata,
        Column("id", String(36), primary_key=True),
        Column("title", String, unique=True, nullable=False),
        Column("image", String, nullable=False)
    )

    users = Table("users", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("email", String, unique=True, nullable=False),
        Column("phone", String),
        Column("password", String, nullable=False),
        Column("type_skin", String),   
        Column("token", String),
        Column("type", Boolean, default=False),         # False = 'user' AND True = 'admin'
    )

    categories = Table("categories", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("images", String, nullable=False),
        Column("is_deleted", Boolean, default=False)

    )

    foods = Table("foods    ", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, nullable=False),
        Column("detail", String),           # same as description
        Column("category_id", ForeignKey(categories.c.id)),
        Column("images", String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
        Column("type_food", String),        # type food
    )

    products = Table("products", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, nullable=False),
        Column("detail", String),           # same as description
        Column("category_id", ForeignKey(categories.c.id)),
        Column("images", String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
        Column("type_product", String),        # type skincare
    )

    metadata.create_all(engine, checkfirst=True)

    return engine, metadata

## ALREADY CALLED
engine, meta = db_init()