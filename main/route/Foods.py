"""
TODO
1. GET Food List
2. GET Food Details
"""

from flask import Blueprint, request, jsonify
from schema.meta import engine,meta
from sqlx import sqlx_easy_orm
from .support import auth_with_token
import pickle

foods_bp = Blueprint("foods",__name__,url_prefix='/')

with open('ml/list_foods.pkl', 'rb') as f:
    df = pickle.load(f)
with open('ml/similarity_foods.pkl', 'rb') as f:
    similarity = pickle.load(f)

@foods_bp.route("/foods", methods=["GET"])
def get_products():
    auth = request.headers.get("authentication")
    def get_product_main(userdata,top=10):
        try:
            index = df[df['skintype'] == userdata.type_skin].index[0]
        except IndexError:
            return(f"No data available for the specified skin type: {userdata.type_skin}")
        distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
        
        print(f"Top {top} Recommendations for {userdata.type_skin} skin type:")
        for i in distances:
            print(f"{df.iloc[i[0]]['name']} ({df.iloc[i[0]]['benefit']})")
        return jsonify ({"message":"Success,Foods Product"}),201 
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


