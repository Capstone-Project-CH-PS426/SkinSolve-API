"""
TODO
1. GET Food List
2. GET Food Details
"""

from flask import Blueprint, request, jsonify
from schema.meta import engine,meta
from sqlx import sqlx_easy_orm
from utils import run_query
from .support import auth_with_token

foods_bp = Blueprint("foods",__name__,url_prefix='/')

@foods_bp.route("/foods", methods=["GET"])
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


@foods_bp.route("/foods/detail", methods=["GET"])
def product_detail_page():
    p = sqlx_easy_orm(engine, meta.tables.get("foods"))

    row = p.get([
        "foods.id",
        "foods.name",
        "foods.nutrition",
        "foods.benefit",
        "foods.images"
    ],
)
    if row is not None:
        foods = row.foods

        if foods is not None:
            data = {}

            data["id"] = foods.id
            data["title"] = foods.name
            data["nutrition"] = foods.nutrition
            data["benefit"] = foods.benefit
            data["images"] = foods.images

            return jsonify({"message": "Success,Product Found","data": data}),200
    return jsonify({"message": "error, product not found"}),404


