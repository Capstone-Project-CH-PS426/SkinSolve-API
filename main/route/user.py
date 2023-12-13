"""
TODO
1. Sign-up
2. Sign-in with JWT
3. User Profile
"""

import jwt
import sqlalchemy as sqlx

from flask import Blueprint, request, jsonify
from valid import Validation
from schema.meta import engine, meta
from sqlx import sqlx_gen_uuid, sqlx_encrypt_pass, sqlx_comp_pass, sqlx_easy_orm
from utils import PasswordChecker, check_password, get_time_epoch_exp, get_value
from .support import auth_with_token

user_bp = Blueprint("user", __name__, url_prefix="")

@user_bp.route("/sign-up", methods=["POST"])
def sign_up():

    payload = request.get_json()

    if payload is not None:

        name = get_value(payload, "name")
        email = get_value(payload, "email")
        phone_number = get_value(payload, "phone_number")
        password = get_value(payload, "password")
        type_skin = get_value(payload, "type_skin")
        skin_problem = get_value(payload, "skin_problem")

        if name is not None and email is not None and password is not None:

            try:

                check_password(password)

                if not Validation.email_address(email):

                    return jsonify({ "message": "error, email not valid" }), 400

                if not Validation.phone_number(phone_number):

                    return jsonify({ "message": "error, phone number not valid" }), 400

                u = sqlx_easy_orm(engine, meta.tables.get("users"))

                if (not u.get(name=name)):

                    if (u.put(id=sqlx_gen_uuid(), name=name, email=email, phone=phone_number, password=sqlx_encrypt_pass(password), type_skin=type_skin, skin_problem=skin_problem)):

                        return jsonify({ "message": "success, user created" }), 201  

                return jsonify({ "message": "error, user already exists" }), 400

            except PasswordChecker as e:

                return jsonify({ "message": "error, " + e.message }), 400

    return jsonify({ "message": "error, bad request" }), 400

@user_bp.route("/sign-in", methods=["POST"])
def sign_in():

    payload = request.get_json()

    if payload is not None:

        email = get_value(payload, "email")
        password = get_value(payload, "password")

        if email is not None and password is not None:

            if not Validation.email_address(email):

                return jsonify({ "message": "error, email not valid" }), 400

            u = sqlx_easy_orm(engine, meta.tables.get("users"))

            userdata = u.get(email=email)

            if (userdata):

                uuid = userdata.id
                name = userdata.name
                email = userdata.email
                phone = userdata.phone
                passcrypt = userdata.password
                usertype_skin = userdata.type_skin
                userskin_problem = userdata.skin_problem


                if sqlx_comp_pass(password, passcrypt):

                    tokenjwt = jwt.encode(
                        payload={
                            "name": name,
                            "exp": get_time_epoch_exp(4) ## just 4 hours activated
                            # "exp": get_time_epoch()
                        },
                        key=uuid ## uuid was randomly generated, and static
                    )

                    if u.update(uuid, token=tokenjwt):

                        return jsonify({ 
                        
                            "user_information": {

                                "name": name,
                                "email": email,
                                "phone_number": phone,
                                "type_skin": usertype_skin,
                                "skin_problem": userskin_problem,
                            },
                            "token": tokenjwt,
                            "message": "success, login success" 
                        }), 200

                    return jsonify({ "message": "error, can`t update jwt token" }), 500

                return jsonify({ "message": "error, wrong password" }), 401

            return jsonify({ "message": "error, user not found" }), 404

    return jsonify({ "message": "error, bad request" }), 400

@user_bp.route("/user", methods=["GET"])
def user_info():

    auth = request.headers.get("authentication")

    def user_info_main(userdata):

        data = {
            "name": userdata.name,
            "email": userdata.email,
            "phone_number": userdata.phone,
            "type_skin": userdata.type_skin,
            "skin_problem": userdata.skin_problem

        }

        return jsonify({

            "data": data,
            "message": "success, authorized"
            
        }), 200

    return auth_with_token(auth, user_info_main)