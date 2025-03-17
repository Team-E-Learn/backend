from time import time
from flask import request
from flask_restful import Resource
from werkzeug.datastructures.structures import ImmutableMultiDict
from backend.database.user import UserTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from lib.jwt.jwt import Jwt

from projenv import JWT_LOGIN_KEY, JWT_LOGIN_EXP


class Login(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Logs in a user with email and password",
            [
                SwagParam(
                    "email",
                    "formData",
                    "string",
                    True,
                    "The email of the user",
                    "example_user@example.com",
                ),
                SwagParam(
                    "password",
                    "formData",
                    "string",
                    True,
                    "The password of the user",
                    "example_password",
                ),
            ],
            [SwagResp(200, "Login successful"), SwagResp(401, "Unauthorized")],
        )
    )
    @Instil("db")
    def post(self, service: SwapDB):
        data: ImmutableMultiDict[str, str] = request.form
        email: str | None = data.get("email")
        password: str | None = data.get("password")

        if email is None or password is None:
            return {"message": "Bad request"}, 400

        user_data = UserTable.get_by_email(service, email)

        if not user_data:
            return {"message": "Bad request"}, 400

        # TODO: Perform database user validation
        if email != "example_user@example.com" and password != "example_password":
            return {"message": "Unauthorized"}, 401

        uid: int = 1  # found user id

        expiry_time: int = int(time()) + JWT_LOGIN_EXP  # 30m from now
        # Logic to authenticate user and generate limited JWT
        limited_jwt: str = (
            Jwt(JWT_LOGIN_KEY)
            .add_claim("iss", "elearn-backend")
            .add_claim("aud", "elearn-login")
            .add_claim("sub", f"{uid}")
            .add_claim("exp", f"{expiry_time}")
            .sign()
        )

        return {"message": "Login successful", "limited_jwt": limited_jwt}, 200
