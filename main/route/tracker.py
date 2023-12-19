"""
TODO!
1. POST FOTO AND ADD NOTES ABOUT SKIN USER
2. POST FOTO AND ADD NOTES ABOUT FOOD USER
3. GET LIST TRACKER
"""
import os
from flask import request,jsonify,Blueprint
from schema.meta import engine,meta
from sqlx import sqlx_easy_orm, sqlx_gen_uuid
from utils import get_images_url_from_column_images,base64_to_image_file
from .support import auth_with_token


tracker_bp = Blueprint("tracker",__name__,url_prefix='/tracker')

@tracker_bp.route("/skin", methods=["POST"])
def tracker_skin():
    auth = request.headers.get("authentication")
    def tracker_main(userdata):
        id = request.json.get("id") or sqlx_gen_uuid
        name = request.json.get("name")
        images = request.json.get("images_skin") or []
        p = sqlx_easy_orm(engine, meta.tables.get("trackers"))
        
        if type(images) is not list:
            images = [ images ]
        ## images is List<Image> as Array<String>
        for image in images:
            if type(image) is not str:
                images.remove(image)
        
        for (index, image) in enumerate([*images]):
            im_filename = str(name + str(index)).lower().replace(" ", "-")
        imagepath = base64_to_image_file(im_filename, image)
        if imagepath is not None:
            images[index] = os.path.join("/image/", os.path.basename(imagepath))

        if p.post(
            id,
            name = name,
            images_skin = ",".join(images)
        ):
            return jsonify({"message": "Photo Addded"}),201
        return jsonify({"message": "Fail added photo"}),406
    return auth_with_token(auth, tracker_main)
        
@tracker_bp.route("/food", methods=["POST"])
def tracker_food():
    auth = request.headers.get("authentication")
    def tracker_main(userdata):
        id = request.json.get("id") or sqlx_gen_uuid
        name = request.json.get("name")
        images = request.json.get("images_foods") or []
        p = sqlx_easy_orm(engine, meta.tables.get("trackers"))
        
        if type(images) is not list:
            images = [ images ]
        ## images is List<Image> as Array<String>
        for image in images:
            if type(image) is not str:
                images.remove(image)
        
        for (index, image) in enumerate([*images]):
            im_filename = str(name + str(index)).lower().replace(" ", "-")
        imagepath = base64_to_image_file(im_filename, image)
        if imagepath is not None:
            images[index] = os.path.join("/image/", os.path.basename(imagepath))

        if p.post(
            id,
            name = name,
            images_foods = ",".join(images)
        ):
            return jsonify({"message": "Photo Addded"}),201
        return jsonify({"message": "Fail added photo"}),406
    return auth_with_token(auth, tracker_main)

@tracker_bp.route("/list", methods=["GET"])
def tracker_list():
    p = sqlx_easy_orm(engine, meta.tables.get("trackers"))

    row = p.get([
        "trackers.id",
        "trackers.images_skin",
        "trackers.images_foods"
    ],
)
    if row is not None:
        trackers = row.trackers

        if trackers is not None:
            data = {}

            data["id"] = trackers.id
            data["images_url_skin"] = get_images_url_from_column_images(trackers.images_skin)
            data["images_url_foods"] = get_images_url_from_column_images(trackers.images_foods)

            return jsonify({"message": "Success,List Found", "data": data}),200
    return jsonify({"message": "error, list not found"}),404

        




