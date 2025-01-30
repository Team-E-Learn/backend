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
