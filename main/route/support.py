import jwt
import sqlalchemy as sqlx

from flask import jsonify
from utils import get_payload_jwt, get_time_epoch
from schema.meta import engine, meta
from sqlx import sqlx_easy_orm
from sqlx.base import DRow
from typing import Callable, Optional

def auth_with_token(auth: Optional[str], fn: Callable):

    if auth is not None:

        timestamp = get_time_epoch()

        header = jwt.get_unverified_header(auth)
        algorithms = header["alg"] if "alg" in header else "HS256"

        payload = get_payload_jwt(auth)

        name = payload["name"] if "name" in payload else None
        expired = payload["exp"] if "exp" in payload else None

        if name is not None and expired is not None:

            u = sqlx_easy_orm(engine, meta.tables.get("users"))

            userdata = u.get(name=name)

            if userdata is not None:

                uuid = userdata.id
                token = userdata.token

                if auth != token:

                    return jsonify({ "message": "error, token not accepted" }), 401

                try:

                    jwt.decode(auth, key=uuid, algorithms=[algorithms])

                    if expired < timestamp:

                        return jsonify({ "message": "error, token was expired" }), 400

                    return fn(userdata)

                except jwt.ExpiredSignatureError as _:

                    return jsonify({ "message": "error, token was expired" }), 400

                ## production
                # except Exception as _:
                    
                #     pass

                except Exception as _:

                    print(_)

                    return jsonify({ "message": "error, something get wrong" }), 500

            return jsonify({ "message": "error, user not found" }), 400

        return jsonify({ "message": "error, token not valid" }), 400

    return jsonify({ "message": "error, bad request" }), 400
