from flask import request
from flask_restful import Resource
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
        data = request.form
        email = data.get('email')
        password = data.get('password')

        # Logic to authenticate user
        if email == "example_user@example.com" and password == "example_password":
            return {"message": "Login successful"}, 200
        else:
            return {"message": "Unauthorized"}, 401