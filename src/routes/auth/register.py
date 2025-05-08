import random
from time import time
from typing import Any, cast
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from backend.database.user import UserTable
from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
from lib.instilled.instiled import Instil
from lib.jwt.jwt import Jwt
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from projenv import JWT_LIMITED_EXP, JWT_LIMITED_KEY


class Register(Resource):
    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Registers a user with email, username, and password",
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
                    "username",
                    "formData",
                    "string",
                    True,
                    "The username of the user",
                    "example_username",
                ),
                SwagParam(
                    "password",
                    "formData",
                    "string",
                    True,
                    "The password of the user",
                    "example_password",
                ),
                SwagParam(
                    "accountType",
                    "formData",
                    "string",
                    True,
                    "The account type of the user (user or teacher)",
                    "user",
                ),
            ],
            [
                SwagResp(200, "Registration successful"),
                SwagResp(400, "Bad Request"),
                SwagResp(404, "Error finding user"),
                SwagResp(409, "Email or username already exists"),
            ],
        )
    )
    @Instil("db")
    def post(self, service: SwapDB):
        # Get email, username, and password from request
        email: str | None = request.form.get("email")
        username: str | None = request.form.get("username")
        password: str | None = request.form.get("password")
        account_type: str | None = request.form.get("accountType")

        # Validate input
        if not email or not username or not password:
            return {"message": "Email, username, and password are required"}, 400

        if account_type not in ["user", "teacher"]:
            return {"message": "Invalid account type"}, 400

        # Check for existing user
        if UserTable.get_by_username(service, username) or UserTable.get_by_email(
            service, email
        ):
            return {"message": "Email or username already exists"}, 409

        # Check if email is verified
        if not UserTable.check_email_verified(service, email):
            return {"message": "Email not verified"}, 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Generate TOTP secret (random 16 char string)
        secret = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=16))

        # Insert user into the database
        user: tuple[Any, ...] | None = UserTable.write_user(
            service,
            account_type,
            email,
            "firstname",
            "lastname",
            username,
            hashed_password,
            secret,
        )

        if not user:
            return {"message": "Error finding user"}, 404

        # Generate expiry time for JWT
        expiry_time: int = int(time()) + JWT_LIMITED_EXP  # 30m from now

        # Logic to authenticate user and generate limited JWT
        token: str = (
            Jwt(JWT_LIMITED_KEY)
            .add_claim("iss", "elearn-backend")
            .add_claim("aud", "elearn-login")
            .add_claim("sub", cast(int, user[0]))
            .add_claim("exp", expiry_time)
            .sign()
        )

        # Return success message and token
        return {
            "message": "Registration successful",
            "user": {
                "id": user[0],
                "email": user[1],
                "username": user[2],
                "secret": secret,
            },
            "token": token,
        }, 200
