from flask import request
from flask_restful import Resource
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from backend.database.user import UserTable

class CheckEmail(Resource):
    def __init__(self, conn):
        self.conn = conn

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Sends a verification code an email if email isn't in use",
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

        # Check if email is in use
        if UserTable.get_by_email(self.conn, email):
            return {"message": "Bad Request"}, 400
        else:
            # Logic to send verification code to email
            verification_code = "123456"
            # Store verification code in DB (example)
            return {"message": "Verification code sent"}, 200
