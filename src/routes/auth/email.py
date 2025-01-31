from flask import request
from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from werkzeug.datastructures.structures import ImmutableMultiDict
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from backend.database.user import UserTable


class CheckEmail(Resource):

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
    @Instil("db")
    def post(self, service: Connection[TupleRow]):
        data: ImmutableMultiDict[str, str] = request.form
        email: str | None = data.get("email")

        if not email:
            return {"message": "Bad Request"}, 400

        # Check if email is in use
        if UserTable.get_by_email(service, email):
            return {"message": "Bad Request"}, 400

        # Logic to send verification code to email
        verification_code: str = "123456"
        # TODO: Send email to email address

        # Store verification code in DB (example)
        return {"message": "Verification code sent"}, 200
