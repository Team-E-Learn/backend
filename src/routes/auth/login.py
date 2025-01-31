from flask import request
from flask_restful import Resource
from werkzeug.datastructures.structures import ImmutableMultiDict
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


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
    def post(self):
        data: ImmutableMultiDict[str, str] = request.form
        email: str | None = data.get("email")
        password: str | None = data.get("password")

        if email is None or password is None:
            return {"message": "Bad request"}, 400

        # Logic to authenticate user and generate limited JWT
        if email == "example_user@example.com" and password == "example_password":
            limited_jwt = "example_limited_jwt"
            return {"message": "Login successful", "limited_jwt": limited_jwt}, 200

        return {"message": "Unauthorized"}, 401
