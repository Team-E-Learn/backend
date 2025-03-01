from flask import request
from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from werkzeug.datastructures.structures import ImmutableMultiDict
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
    def post(self, service: Connection[TupleRow]):
        data: ImmutableMultiDict[str, str] = request.form
        email: str | None = data.get("email")
        token: str | None = data.get("token")

        if not email or not token:
            return {"message": "Bad Request"}, 400

        # Logic to verify email token
        if token != EmailCodesTable.get_code(service, email):
            return {"message": "Bad Request"}, 400

        EmailCodesTable.verify_email(service, email)
        return {"message": "Email verified"}, 200
