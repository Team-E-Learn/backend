from time import time
from typing import cast
from flask import request
from flask_restful import Resource
from werkzeug.security import check_password_hash
from backend.auth import get_jwt, get_jwt_sub
from backend.database.user import UserTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from lib.jwt.jwt import Jwt, JwtValidator
from projenv import JWT_LIMITED_KEY, JWT_LIMITED_EXP


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
            [
                SwagResp(200, "Login successful"),
                SwagResp(400, "Bad request"),
                SwagResp(401, "Unauthorized"),
            ],
            protected=True,
        )
    )
    @Instil("db")
    def post(self, service: SwapDB):
        # Get email and password from request
        email: str | None = request.form.get("email")
        password: str | None = request.form.get("password")

        # Check if email and password are provided
        # If not, return a 400 Bad Request
        if email is None or password is None:
            return {"message": "Bad request"}, 400

        # Check if user exists
        user_data = UserTable.get_by_email(service, email)

        # If not, return a 400 Bad Request
        if not user_data:
            return {"message": "Bad request"}, 400

        # Check if the password is correct
        # If not, return a 401 Unauthorized
        if not check_password_hash(cast(str, user_data[6]), password):
            return {"message": "Unauthorized"}, 401

        # Get user id
        uid: int = cast(int, user_data[0])

        # Generate expiry time for JWT
        expiry_time: int = int(time()) + JWT_LIMITED_EXP  # 30m from now

        # Logic to authenticate user and generate limited JWT
        token: str = (
            Jwt(JWT_LIMITED_KEY)
            .add_claim("iss", "elearn-backend")
            .add_claim("aud", "elearn-login")
            .add_claim("sub", uid)
            .add_claim("exp", expiry_time)
            .sign()
        )

        # Return limited JWT (for 2FA) and success message
        return {"message": "Login successful", "limited_jwt": token}, 200
