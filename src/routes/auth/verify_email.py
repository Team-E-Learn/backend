from flask import request
from flask_restful import Resource
from werkzeug.datastructures.structures import ImmutableMultiDict
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from backend.database.email_codes import EmailCodesTable


class VerifyEmail(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Verifies a user's email with a 6 digit code",
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

    @Instil("db")
    def post(self, service: SwapDB):
        # Get email and token from request
        email: str | None = request.form.get("email")
        token: str | None = request.form.get("token")

        # Check if email and token are provided, if not return a 400 Bad Request
        if not email or not token:
            return {"message": "Bad Request"}, 400

        # Logic to verify email token
        if token != EmailCodesTable.get_code(service, email):
            return {"message": "Bad Request"}, 400

        # Set email as verified
        EmailCodesTable.set_verified(service, email)

        # Return 200 on successful email verification
        return {"message": "Email verified"}, 200
