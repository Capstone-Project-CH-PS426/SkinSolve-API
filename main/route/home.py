#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Todo ! 
1. Search Page Product
2. Get Saved List
"""

from flask import Blueprint, jsonify, request
from utils import run_query
from .support import auth_with_token

home_bp = Blueprint("home", __name__, url_prefix="/home")

@home_bp.route("/search_products", methods=["GET","POST"])
def search_page():
    name = request.get_json()
    data = run_query(f"SELECT * FROM products ORDER BY name LIKE '{name}'")
    if data is None:
        return jsonify({"message":"Product Not Found"}),404
    else:
        return jsonify({"message": "Success", "data": data}),201
    

@home_bp.route("/savedlist", methods=["GET"])
def get_saved_list():
    auth = request.headers.get("authentication")

    def get_saved_main(userdata):
        raw_data = run_query(f"SELECT id, name, detail, images, type_product FROM products WHERE user_id = '{userdata.id}'")
        data = []
        for item in raw_data:
            req = {
                "id": item["id"],
                "name": item["name"],
                "details": item["details"]
            }
            data.append(req)
        return jsonify({ "data": data, "message": "success, list found" }), 200

    return auth_with_token(auth, get_saved_main)