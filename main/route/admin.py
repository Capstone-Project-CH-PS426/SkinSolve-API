"""
TODO
1. Create Recomendation Product
2. Create Recommendation Food
3. Delete Recommendation Product
4. Delete Recommendation Food
"""

import os
import sqlalchemy as sqlx
from sqlx import sqlx_easy_orm, sqlx_gen_uuid

from flask import Blueprint, request, jsonify
from .support import auth_with_token
from schema.meta import engine, meta
from utils import get_images_url_from_column_images, get_sort_columns, get_sort_rules, is_admin, parse_num, sqlx_rows_norm_expand, base64_to_image_file, convert_epoch_to_datetime, run_query

admin_bp = Blueprint("admin", __name__, url_prefix="")

"""
sort_by Price a_z, Price z_a

page 1

page_size 25

is_admin True(boolean)

Created_at
User_id
email

data
{
    "data": [
   	 {
   		 "id": "uuid",
   		 "title": "Nama product",
   		 "size": [
   			 "S",
   			 "M",
   			 "L"
   		 ],
   		 "created_at": "Tue, 25 august 2022",
   		 "product_detail": "lorem ipsum",
   		 "email": "raihan@gmail.com",
   		 "images_url": [
   			 "/image/image1",
   			 "/image/image2"
   		 ],
   		 "user_id": "uuid",
   		 "total": 1000
   	 }
    ]
}

"""

@admin_bp.route("/products", methods=["POST"])
def products_page():

    auth = request.headers.get("authentication")

    def products_page_main(userdata):

        if not is_admin(userdata):

            return jsonify({ "message": "error, unauthorized account" }), 401

        product_name = request.json.get("product_name")
        description = request.json.get("description")
        images = request.json.get("images") or [] 
        type_product = request.json.get("type_product")
        category_id = request.json.get("category")
        
        ctg_safe = [x["id"] for x in run_query("SELECT id FROM categories WHERE is_deleted != true")]
        
        if category_id not in ctg_safe or category_id == "":
            return jsonify({ "message": "error, category not found"}), 404
    
        p = sqlx_easy_orm(engine, meta.tables.get("products"))

        if type(images) is not list:

            images = [ images ]

        ## images is List<Image> as Array<String>
        for image in images:

            if type(image) is not str:

                images.remove(image)

        ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        ## default condition

        if type(type_product) is None:

            type_product = ""

        if not p.get(p.c.name == product_name):

            product_id = sqlx_gen_uuid()

            for (index, image) in enumerate([*images]):

                im_filename = str(product_name + str(index)).lower().replace(" ", "-")

                imagepath = base64_to_image_file(im_filename, image)

                if imagepath is not None:

                    ## change route from /images to /image
                    images[index] = os.path.join("/image/", os.path.basename(imagepath))
                    continue
                
                images[index] = image

            if type(type_product) is str:

                type_product = type_product.lower()

            if p.post(
                product_id, 
                name = product_name, 
                detail = description, 
                category_id = category_id, 
                images = ",".join(images),
                type_product = type_product,
                is_deleted = False 
            ):

                return jsonify({ "message": "Product added" }), 201

            return jsonify({ "message": "error, product fail added"}), 406 ## di tolak

        # return jsonify({ "message": "success, product has been added" }), 200
        return jsonify({ "message": "error, product already exists" }), 400

    return auth_with_token(auth, products_page_main)

@admin_bp.route("/products", methods=["PUT"])
def products_update_page():

    """
    product_name Product 1
    
    description Lorem ipsum
    
    images [image_1, image_2, image_3]
    
    condition new
    
    category category_id
    
    price 10000

    product_id product_id
    """

    auth = request.headers.get("authentication")

    def products_update_page_main(userdata):

        if not is_admin(userdata):

            return jsonify({ "message": "error, unauthorized account" }), 401

        product_id = request.json.get("product_id")
        # prd_info = run_query(f"SELECT * FROM products WHERE id = '{product_id}'")[0]
        # try:
        product_name = request.json.get("product_name")
        #     product_name = request.json.get("product_name")
        #     if product_name == "":
        #         return jsonify({ "message": "error, invalid name" }), 400
        # except:
        #     product_name = prd_info["name"]
        # try:
        description = request.json.get("description")
        #     description = request.json.get("description")
        # except:
        #     description = prd_info["detail"]
        # try:
        images = request.json.get("images")
        #     images = request.json.get("images") # or [] ## base64 decode save as file in folder
        # except:
        #     images = prd_info["images"]
        # try:
        type_product = request.json.get("type_product")
        #     condition = request.json.get("condition").lower()
        #     if condition not in ["new", "used"]:
        #         return jsonify({ "message": "error, invalid condition" }), 400
        # except:
        #     condition = prd_info["condition"]
        # try:
        category_id = request.json.get("category")
        #     category_id = request.json.get("category")
        ctg_safe = [x["id"] for x in run_query("SELECT id FROM categories WHERE is_deleted != true")]
        if category_id not in ctg_safe:
            return jsonify({ "message": "error, category not found"}), 404
        # except:
        #     category_id = prd_info["category_id"]
        

        if type(product_id) is not str \
            or product_id == '':
            
            return jsonify({ "message": "error, product_id not found" }), 400
        
        p = sqlx_easy_orm(engine, meta.tables.get("products"))

        if type(images) is not list:

            images = [ images ]

        ## images is List<Image> as Array<String>
        for image in images:

            if type(image) is not str:

                images.remove(image)

        ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        product = p.get(product_id)

        if product:

            for (index, image) in enumerate([*images]):

                if image.startswith("data:"):

                    im_filename = str(product_name + str(index)).lower().replace(" ", "-")

                    imagepath = base64_to_image_file(im_filename, image)

                    if imagepath is not None:

                        ## change route from /images to /image
                        images[index] = os.path.join("/image/", os.path.basename(imagepath))
                        continue
                    
                    images[index] = image

            if type(product_name) is None:

                product_name = product.name

            if type(description) is None:

                description = product.description

            if type(images) is None \
                or not images:

                images = get_images_url_from_column_images(product.images)

            if type(type_product) is None:

                type_product = product.type_product

            if type(condition) is str:

                condition = condition.lower()

            if p.update(
                product_id, 
                name = product_name, 
                detail = description, 
                category_id = category_id, 
                images = ",".join(images),
                type_product = type_product
            ):

                return jsonify({ "message": "Product updated" }), 201

            return jsonify({ "message": "error, product failed to update"}), 406 ## di tolak

        return jsonify({ "message": "error, product unknown" }), 200

    return auth_with_token(auth, products_update_page_main)

@admin_bp.route("/categories",methods=["POST"])
def category():
    auth = request.headers.get("Authentication")

    def create_category(userdata):
        if not is_admin(userdata):
            return jsonify({"message": "error, unauthorized account"}), 401
        try:
            id = request.json.get("id") or sqlx_gen_uuid()
            name = request.json.get("category_name")
            if name == '':
                 return jsonify({"message": "error, invalid name"}), 400
            # images = request.json.get("images") ## base64 decode save as file in folder
            is_deleted = request.json.get("is_deleted") or False
        except:
            return jsonify({"message": "Bad Request"}), 400
        
        # if type(images) is not list:
        #     images = [ images ]
        # ## images is List<Image> as Array<String>
        # for images in images:
        #     if type(images) is not str:
        #         images.remove(images)
        
        if run_query(f"SELECT * FROM categories WHERE name='{name}'") == []:
            run_query(f"INSERT INTO categories (id, name, images, is_deleted) VALUES ('{id}', '{name}', '', '{is_deleted}')", True)
            return jsonify({"message": "Category added"}), 200
        else:
            return jsonify({"message": "error, category already exists"}), 400
            
    return auth_with_token(auth, create_category)

@admin_bp.route("/categories/<string:category_id>",methods=["PUT"])
def update_category_page(category_id):
    auth = request.headers.get("Authentication")
    cat_id = category_id

    def update_category(userdata):
        if not is_admin(userdata):
            return jsonify({"message": "error, unauthorized account"}), 401
        try:
            # id = request.json.get("category_id")
            name = request.json.get("category_name")
            # images = request.json.get("images") or [] ## base64 decode save as file in folder
            # is_deleted = request.json.get("is_deleted")
        except:
            return jsonify({"message": "Bad Request"}), 400

        # if type(images) is not list:
        #     images = [ images ]
        # ## images is List<Image> as Array<String>
        # for images in images:
        #     if type(images) is not str:
        #         images.remove(images)

        if run_query(f"SELECT * FROM categories WHERE id='{cat_id}'") != []:
            run_query(f"UPDATE categories SET name='{name}' WHERE id='{cat_id}'", True)
            return jsonify({"message": "Category updated"}), 200
        else:
            return jsonify({"message": "error, invalid id"}), 400
            
    return auth_with_token(auth, update_category)
