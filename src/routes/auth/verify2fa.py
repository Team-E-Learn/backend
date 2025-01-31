from flask import request
from flask_restful import Resource
from werkzeug.datastructures.structures import ImmutableMultiDict
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Verify2FA(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Auth"],
            "Verifies a user with a 6-digit 2FA code",
            [
                SwagParam(
                    "code",
                    "formData",
                    "string",
                    True,
                    "The 6-digit 2FA code",
                    "123456",
                ),
            ],
            [SwagResp(200, "Verification successful"), SwagResp(401, "Unauthorized")],
        )
    )
    def post(self):
        data: ImmutableMultiDict[str, str] = request.form
        code: str | None = data.get("code")

        if not code:
            return {"message": "Bad Request"}, 400

        # Logic to verify 2FA code and generate full access JWT
        if code != "123456":  # Example verification logic
            return {"message": "Unauthorized"}, 401

        full_access_jwt = "example_full_access_jwt"
        return {
            "message": "Verification successful",
            "full_access_jwt": full_access_jwt,
        }, 200
