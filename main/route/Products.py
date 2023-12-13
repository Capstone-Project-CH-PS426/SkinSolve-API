"""
TODO
1. GET Product List By User Skin Type
2. GET Product Details
"""

from flask import Blueprint, request, jsonify
from schema.meta import engine,meta
from sqlx import sqlx_easy_orm
from utils import run_query
from .support import auth_with_token

products_bp = Blueprint("products", __name__, url_prefix="/")

@products_bp.route("/products", methods=["GET"])
def get_products():
    auth = request.headers.get("authentication")
    def get_product_main(userdata):
        if userdata.type_skin == "Oil":
            data = run_query("SELECT * FROM products WHERE skin_type LIKE 'Oi%'")
            return ({"data": data, "message":"Success"}),201
        if userdata.type_skin == "Dry":
            data = run_query("SELECT * FROM products WHERE skin_type LIKE 'Dr%'")
            return ({"data": data, "message":"Success"}),201
        if userdata.type_skin == "Normal":
            data = run_query("SELECT * FROM products WHERE skin_type LIKE 'Nor%'")
            return ({"data": data, "message":"Success"}),201
        if userdata.type_skin == "Combination":
            data = run_query("SELECT * FROM products WHERE skin_type LIKE 'Combi%'")
            return ({"data": data, "message":"Success"}),201
        if userdata.type_skin == "Sensitive":
            data = run_query("SELECT * FROM products WHERE skin_type LIKE 'Sensiti%'")
            return ({"data": data, "message":"Success"}),201
        else:
            return jsonify ({"message": "Not Found"}),404
    return auth_with_token(auth,get_product_main)

@products_bp.route("/products/detail", methods=["GET"])
def product_detail_page():
    p = sqlx_easy_orm(engine, meta.tables.get("products"))

    row = p.get([
        "products.id",
        "products.name",
        "products.brand",
        "products.type_product",
        "products.composisition"
    ],
)
    if row is not None:
        products = row.products

        if products is not None:
            data = {}

            data["id"] = products.id
            data["title"] = products.name
            data["brand"] = products.brand
            data["type_product"] = products.type_product
            data["composisition"] = products.composisition

            return jsonify({"message": "Success,Product Found","data": data}),200
    return jsonify({"message": "error, product not found"}),404
