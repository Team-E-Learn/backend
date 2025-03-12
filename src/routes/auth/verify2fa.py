from mintotp import totp
from flask import request
from flask_restful import Resource
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
                    "Limited JWT",
                    "header",
                    "string",
                    True,
                    "The limited JWT",
                    "Bearer example_limited_jwt",
                ),
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
        limited_jwt: str | None = request.form.get("Limited JWT")
        code: str | None = request.form.get("code")

        # TODO:
        # 1) Take user limited JWT
        # 2) Validate
        # 3) Ensure uid in jwt sub is valid
        # 4) Check 2fa code valid
        # 5) Produce new JWT with full access (see /auth/login)

        if not limited_jwt or not code:
            return {"message": "Bad Request"}, 400

        print(limited_jwt)
        # Resolve limited_jwt to user secret

        # Logic to verify 2FA code and generate full access JWT
        if totp("TODO USER CODE") != code:
            return {"message": "Unauthorized"}, 401

        full_access_jwt = "example_full_access_jwt"
        return {
            "message": "Verification successful",
            "full_access_jwt": full_access_jwt,
        }, 200
