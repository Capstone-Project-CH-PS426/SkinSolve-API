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


@home_bp.route("/search_products", methods=["GET"])
def search_page():
    auth = request.headers.get("authentication")
    def search_page_main():
        data = run_query("SELECT * FROM products")
        return jsonify({"data": data, "message" : "success, product found"}),200
    return auth_with_token(auth,search_page_main)
    

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