import random
from time import time
from tokenize import String
from typing import Any
from flask import request
from flask_restful import Resource
from werkzeug.datastructures.structures import ImmutableMultiDict
from werkzeug.security import generate_password_hash
from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
from lib.instilled.instiled import Instil
from lib.jwt.jwt import Jwt
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from projenv import JWT_LOGIN_EXP, JWT_LOGIN_KEY


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
            ],
            [
                SwagResp(200, "Registration successful"),
                SwagResp(400, "Bad Request"),
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

        # Validate input
        if not email or not username or not password:
            return {"message": "Email, username, and password are required"}, 400

        # Check for existing user
        cursor: SwapCursor = service.get_cursor()
        user_result: SwapResult = cursor.execute(
            StringStatement(
                "SELECT userID FROM users WHERE email = %s OR username = %s"
            ),
            (email, username),
        )

        if user_result.fetch_one():
            return {"message": "Email or username already exists"}, 409

        # Check if email is verified
        email_result: SwapResult = cursor.execute(
            StringStatement("""SELECT verified FROM email_codes WHERE email = %s"""),
            (email,),
        )
        email_tup: tuple[bool] | None = email_result.fetch_one()
        if email_tup is None or not email_tup[0]:
            return {"message": "Email not verified"}, 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Generate TOTP secret (random 16 char string)
        secret = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=16))

        # Insert user into the database
        insert_result: SwapResult = cursor.execute(
            StringStatement(
                """
                        INSERT INTO users (accountType, email, firstname, lastname, username, password, totpSecret)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING userID, email, username
                """
            ),
            ("user", email, "firstname", "lastname", username, hashed_password, secret),
        )
        user: tuple[Any, ...] | None = insert_result.fetch_one()
        service.commit()

        if not user:
            return {"message": "Error finding user"}, 500

        # Generate expiry time for JWT
        expiry_time: int = int(time()) + JWT_LOGIN_EXP  # 30m from now

        # Logic to authenticate user and generate limited JWT
        token: str = (
            Jwt(JWT_LOGIN_KEY)
            .add_claim("iss", "elearn-backend")
            .add_claim("aud", "elearn-login")
            .add_claim("sub", f"{user[0]}")
            .add_claim("exp", f"{expiry_time}")
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
