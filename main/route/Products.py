"""
TODO
1. GET Product List By User Skin Type
2. GET Product Details
"""

from flask import Blueprint, request, jsonify
from schema.meta import engine,meta
from sqlx import sqlx_easy_orm
from .support import auth_with_token
import pickle

products_bp = Blueprint("products", __name__, url_prefix="/")

with open('ml/list_products.pkl', 'rb') as f:
    df = pickle.load(f)
with open('ml/similarity_products.pkl', 'rb') as f:
    similarity = pickle.load(f)

@products_bp.route("/product", methods=["GET"])
def product():
    auth = request.headers.get("authentication")
    def get_product_main(userdata,top=10):
        try:
            index = df[df['skintype'] == userdata.type_skin].index[0]
        except IndexError:
            return(f"No data available for the specified skin type: {userdata.type_skin}")
        distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
        
        print(f"Top {top} Recommendations for {userdata.type_skin} skin type:")
        for i in distances:
            print(f"{df.iloc[i[0]]['name']} ({df.iloc[i[0]]['type']})")
        return jsonify ({"message":"Success,Found Product"}),201 
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
