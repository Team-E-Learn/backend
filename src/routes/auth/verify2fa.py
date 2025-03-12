import base64
import json
from time import time

from mintotp import totp
from flask import request
from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from backend.database.user import UserTable
from lib.instilled.instiled import Instil
from lib.jwt.jwt import Jwt
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from projenv import JWT_ACCESS_KEY, JWT_ACCESS_EXP


class Verify2FA(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Verifies a user with a 6-digit 2FA code",
            [
                SwagParam(
                    "Limited JWT",
                    "formData",
                    "string",
                    True,
                    "The limited JWT",
                    "Bearer example_limited_jwt",
                ),
                SwagParam(
                    "code",
                    "formData",
                    "string",
                    True,
                    "The 6-digit 2FA code",
                    "123456",
                ),
            ],
            [SwagResp(200, "Verification successful"), SwagResp(401, "Unauthorized")],
        )
    )
    @Instil("db")
    def post(self, service: Connection[TupleRow]):
        limited_jwt: str | None = request.form.get("Limited JWT")
        code: str | None = request.form.get("code")

        if not limited_jwt or not code:
            return {"message": "Bad Request"}, 400


        # decode limited JWT to get user ID and check expiry time
        payload = limited_jwt.split(".")[1]
        # make sure payload is padded correctly
        if len(payload) % 4 != 0:
            payload += "=" * (4 - len(payload) % 4)
        payload = base64.b64decode(payload)
        payload = json.loads(payload)
        user_id = payload["sub"]
        expiry_time = payload["exp"]

        if int(expiry_time) < int(time()):
            return {"message": "Unauthorized"}, 401

        # get user secret from database
        user_secret: str = UserTable.get_totp_secret(service, user_id)

        # if user secret is not found, return unauthorized
        if not user_secret:
            return {"message": "Unauthorized"}, 401

        # Logic to verify 2FA code and generate full access JWT
        if totp(user_secret) != code:
            return {"message": "Unauthorized"}, 401

        expiry_time: int = int(time()) + JWT_ACCESS_EXP

        # Produce new JWT with full access
        full_access_jwt: str = (
            Jwt(JWT_ACCESS_KEY)
            .add_claim("iss", "elearn-backend")
            .add_claim("aud", "elearn-access")
            .add_claim("sub", f"{user_id}")
            .add_claim("exp", f"{expiry_time}")
            .sign()
        )

        # return full access JWT
        return {
            "message": "Verification successful",
            "full_access_jwt": full_access_jwt,
        }, 200
