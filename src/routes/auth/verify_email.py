from flask import request
from flask_restful import Resource
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class VerifyEmail(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Verifies a user's email with a 6 digit code",
            [
                SwagParam(
                    "token",
                    "formData",
                    "string",
                    True,
                    "The verification token",
                    "123456",
                ),
            ],
            [SwagResp(200, "Email verified"), SwagResp(400, "Bad Request")],
        )
    )
    def post(self):
        data = request.form
        token = data.get('token')

        # Logic to verify email token
        if token == "123456":  # Example verification logic
            return {"message": "Email verified"}, 200
        else:
            return {"message": "Bad Request"}, 400

class ConfirmEmail(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Sends a verification code to the user's email",
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
            [SwagResp(200, "Verification code sent"), SwagResp(400, "Bad Request")],
        )
    )
    def post(self):
        data = request.form
        email = data.get('email')

        # Logic to send verification code to email
        if email:  # Example logic
            verification_code = "123456"
            # Store verification code in DB (example)
            return {"message": "Verification code sent"}, 200
        else:
            return {"message": "Bad Request"}, 400