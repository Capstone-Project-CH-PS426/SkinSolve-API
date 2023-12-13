#!/usr/bin/env python3
#-*- coding: utf-8 -*-


from utils import call_engine, call_local_engine
from sqlalchemy import MetaData, Table, Column, String, Boolean, ForeignKey, Integer, BigInteger, text

def db_init():

    engine = call_engine()
    # engine = call_local_engine()

    metadata = MetaData()

    users = Table("users", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("email", String, unique=True, nullable=False),
        Column("phone", String),
        Column("password", String, nullable=False),
        Column("type_skin", String),
        Column("skin_problem", String),
        Column("images", String),
        Column("notes", String),    
        Column("token", String),
    )

    foods = Table("foods", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id)),
        Column("name", String, nullable=False),
        Column("detail", String), # same as description
        Column("nutrition", String), 
        Column("skin_type", String),        # type food          
        Column("benefit", String),
        Column("images", String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
    )

    products = Table("products", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id)),
        Column("name", String, nullable=False),
        Column("detail", String), # same as description
        Column("brand", String),\
        Column("type_product", String),        # type skincare
        Column("composisition", String),        
        Column("skin_type", String),          
        Column("images", String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
    )

    # IGNORE THIS COLUMN
    test = Table("test", metadata,
        Column("name", String(36), primary_key=True),
    )

    metadata.create_all(engine, checkfirst=True)

    return engine, metadata

## ALREADY CALLED
engine, meta = db_init()