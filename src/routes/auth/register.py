from flask import request
from flask_restful import Resource
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class RegisterEmail(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Registers a user with an email",
            [
                SwagParam(
                    "email",
                    "formData",
                    "string",
                    True,
                    "The email of the user",
                    "example_user@example.com",
                ),
            ],
            [SwagResp(200, "Registration successful"), SwagResp(400, "Bad Request")],
        )
    )
    def post(self):
        data = request.form
        email = data.get('email')

        # Logic to register user
        if email:  # Example registration logic
            return {"message": "Registration successful"}, 200
        else:
            return {"message": "Bad Request"}, 400

class VerifyEmail(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Verifies a user's email",
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
                    "code",
                    "formData",
                    "string",
                    True,
                    "The verification code",
                    "123456",
                ),
            ],
            [SwagResp(200, "Verification successful"), SwagResp(400, "Bad Request")],
        )
    )
    def post(self):
        data = request.form
        email = data.get('email')
        code = data.get('code')

        # Logic to verify email
        if email and code == "123456":  # Example verification logic
            return {"message": "Verification successful"}, 200
        else:
            return {"message": "Bad Request"}, 400

class Username(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Checks if a username is available",
            [
                SwagParam(
                    "username",
                    "formData",
                    "string",
                    True,
                    "The username to check",
                    "example_username",
                ),
            ],
            [SwagResp(200, "Username available"), SwagResp(400, "Bad Request"), SwagResp(409, "Username taken")],
        )
    )
    def post(self):
        data = request.form
        username = data.get('username')

        # Logic to check username availability
        if username == "example_username":  # Example logic
            return {"message": "Username taken"}, 409
        elif username:
            return {"message": "Username available"}, 200
        else:
            return {"message": "Bad Request"}, 400

class Password(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Sets a password for a user",
            [
                SwagParam(
                    "password",
                    "formData",
                    "string",
                    True,
                    "The password of the user",
                    "example_password",
                ),
            ],
            [SwagResp(200, "Password set successfully"), SwagResp(400, "Bad Request")],
        )
    )
    def post(self):
        data = request.form
        password = data.get('password')

        # Logic to set password
        if password:  # Example password setting logic
            return {"message": "Password set successfully"}, 200
        else:
            return {"message": "Bad Request"}, 400