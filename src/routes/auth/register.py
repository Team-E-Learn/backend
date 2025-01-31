from flask import request
from flask_restful import Resource
from werkzeug.datastructures.structures import ImmutableMultiDict
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


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
            [SwagResp(200, "Registration successful"), SwagResp(400, "Bad Request")],
        )
    )
    def post(self):
        data: ImmutableMultiDict[str, str] = request.form
        email: str | None = data.get("email")
        username: str | None = data.get("username")
        password: str | None = data.get("password")

        # Logic to register user and generate TOTP token
        if email and username and password:  # Example registration logic
            totp_token = "example_totp_token"
            return {"message": "Registration successful", "totp_token": totp_token}, 200

        return {"message": "Bad Request"}, 400
