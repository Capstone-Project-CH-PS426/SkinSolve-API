"""
TODO!
1. POST FOTO AND ADD NOTES ABOUT SKIN USER
2. POST FOTO AND ADD NOTES ABOUT FOOD USER
3. GET LIST TRACKER
"""

from flask import request,jsonify,Blueprint
from utils import run_query
from .support import auth_with_token


tracker_bp = Blueprint("tracker",__name__,url_prefix='/')

# @tracker_bp.route("/skin", methods=["GET","POST"])
# def tracker_skin():
#     auth = request.headers.get("authentication")
#     def tracker_skin_main(userdata):
#         return

# @tracker_bp.route("/food", methods=["GET","POST"])
# def tracker_food():
#     auth = request.headers.get("authentication")
#     def tracker_skin_main(userdata):
#         return

@tracker_bp.route("/", methods=["GET"])
def tracker_list():
    auth = request.headers.get("authentication")
    def tracker_list_main(userdata):
        data = {
            "image": userdata.images,
            "notes": userdata.notes
        }
        return jsonify({"data": data, "message": "Success"}),201
    return auth_with_token(auth, tracker_list_main)


