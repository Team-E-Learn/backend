from flask import request
from flask_restful import Resource
from werkzeug.datastructures.structures import ImmutableMultiDict
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg.connection import Connection
from psycopg import sql
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
import jwt
import datetime
import os

class Register(Resource):
    def __init__(self, conn: Connection):
        self.conn = conn

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
    def post(self):
        data: ImmutableMultiDict[str, str] = request.form
        email: str | None = data.get("email")
        username: str | None = data.get("username")
        password: str | None = data.get("password")

        # Validate input
        if not email or not username or not password:
            return {"message": "Email, username, and password are required"}, 400

        # Check for existing user
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    sql.SQL("""
                        SELECT id FROM users WHERE email = %s OR username = %s
                    """),
                    (email, username)
                )
                if cur.fetchone():
                    return {"message": "Email or username already exists"}, 409
        except Exception as e:
            return {"message": f"Database error: {str(e)}"}, 500

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    sql.SQL("""
                        INSERT INTO users (email, username, password)
                        VALUES (%s, %s, %s)
                        RETURNING id, email, username
                    """),
                    (email, username, hashed_password)
                )
                user = cur.fetchone()
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return {"message": f"Registration failed: {str(e)}"}, 500

        # Generate JWT token
        token = jwt.encode(
            {
                "user_id": user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            os.getenv("JWT_SECRET", "default_secret"),
            algorithm="HS256",
        )

        return {
            "message": "Registration successful",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
            },
            "token": token,
        }, 200