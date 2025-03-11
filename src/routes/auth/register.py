from time import time
from flask import request
from flask_restful import Resource
from psycopg.rows import TupleRow
from werkzeug.datastructures.structures import ImmutableMultiDict
from werkzeug.security import generate_password_hash
from psycopg.connection import Connection
from psycopg import sql
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
    def post(self, service: Connection[TupleRow]):
        email: str | None = request.form.get("email")
        username: str | None = request.form.get("username")
        password: str | None = request.form.get("password")

        # Validate input
        if not email or not username or not password:
            return {"message": "Email, username, and password are required"}, 400

        # Check for existing user
        try:
            with service.cursor() as cur:
                _ = cur.execute(
                    sql.SQL("""SELECT userID FROM users WHERE email = %s OR username = %s"""),
                    (email, username),
                )
                if cur.fetchone():
                    return {"message": "Email or username already exists"}, 409
        except Exception as e:
            return {"message": f"Database error: {str(e)}"}, 500

        # Check if email is verified
        with service.cursor() as cur:
            _ = cur.execute(
                sql.SQL("""SELECT verified FROM email_codes WHERE email = %s"""),
                (email,),
            )
            result = cur.fetchone()
            if result is None or not result[0]:
                return {"message": "Email not verified"}, 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        try:
            with service.cursor() as cur:
                _ = cur.execute(
                    sql.SQL(
                        """
                        INSERT INTO users (accountType, email, firstname, lastname, username, password)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING userID, email, username
                    """
                    ),
                    ("user", email, "firstname", "lastname", username, hashed_password),
                )
                user: TupleRow | None = cur.fetchone()
                service.commit()
        except Exception as e:
            service.rollback()
            return {"message": f"Registration failed: {str(e)}"}, 500

        if not user:
            return {"message": "Error finding user"}, 500

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

        return {
            "message": "Registration successful",
            "user": {
                "id": user[0],
                "email": user[1],
                "username": user[2],
            },
            "token": token,
        }, 200
