from flask import request
from flask_restful import Resource
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class CheckEmail(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Auth"],
            "Checks if an email exists",
            [
                SwagParam(
                    "email",
                    "query",
                    "string",
                    True,
                    "The email to check",
                    "example_user@example.com",
                ),
            ],
            [SwagResp(200, "Email exists"), SwagResp(400, "Bad Request"), SwagResp(404, "Email not found")],
        )
    )
    def get(self):
        email = request.args.get('email')

        # Logic to check email existence
        if email == "example_user@example.com":  # Example logic
            return {"message": "Email exists"}, 200
        elif email:
            return {"message": "Email not found"}, 404
        else:
            return {"message": "Bad Request"}, 400

class CheckUsername(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Auth"],
            "Checks if a username exists",
            [
                SwagParam(
                    "username",
                    "query",
                    "string",
                    True,
                    "The username to check",
                    "example_username",
                ),
            ],
            [SwagResp(200, "Username exists"), SwagResp(400, "Bad Request"), SwagResp(404, "Username not found")],
        )
    )
    def get(self):
        username = request.args.get('username')

        # Logic to check username existence
        if username == "example_username":  # Example logic
            return {"message": "Username exists"}, 200
        elif username:
            return {"message": "Username not found"}, 404
        else:
            return {"message": "Bad Request"}, 400

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
        data = request.form
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Logic to register user and generate TOTP token
        if email and username and password:  # Example registration logic
            totp_token = "example_totp_token"
            return {"message": "Registration successful", "totp_token": totp_token}, 200
        else:
            return {"message": "Bad Request"}, 400