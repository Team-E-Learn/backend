from flask import request
from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from backend.database.user import UserTable
from backend.database.email_codes import EmailCodesTable
from requests import post, Response
from random import choice
from projenv import EMAIL_API_TOKEN


def send_verification_email(to_email: str, verification_code: str) -> bool:
    url: str = "https://cartervernon.com/elearn-script.php"
    payload: dict[str, str] = {
        "auth_key": EMAIL_API_TOKEN,
        "email": to_email,
        "code": verification_code,
    }

    response: Response = post(url, data=payload)
    return response.status_code == 200


def generate_code() -> str:
    return "".join([choice("0123456789") for _ in range(6)])


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
        # Get email from request
        email: str | None = request.form.get("email")

        # Check if email is provided, if not return a 400 Bad Request
        if not email:
            return {"message": "Bad Request"}, 400

        # Check if email is in use
        if UserTable.get_by_email(service, email):
            return {"message": "Bad Request"}, 400

        # Logic to send verification code to email
        verification_code: str = generate_code()

        # Send verification code to email
        if not send_verification_email(email, verification_code):
            return {"message": "Failed to send email"}, 400

        # Store verification code in DB
        EmailCodesTable.add_code(service, email, verification_code)

        # Return success message
        return {"message": "Verification code sent"}, 200
