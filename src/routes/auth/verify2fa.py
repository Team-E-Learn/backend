import base64
import json
from time import time
from backend.auth import get_jwt
from lib.dataswap.database import SwapDB
from mintotp import totp
from flask import request
from flask_restful import Resource
from backend.database.user import UserTable
from lib.instilled.instiled import Instil
from lib.jwt.jwt import ALLOWED_CLAIM_DATA, Jwt, JwtValidator
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from projenv import JWT_ACCESS_KEY, JWT_ACCESS_EXP


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
                    "number",
                    True,
                    "The 6-digit 2FA code",
                    "123456",
                ),
            ],
            [SwagResp(200, "Verification successful"), SwagResp(400, "Bad Request"),
             SwagResp(401, "Unauthorized")],
        )
    )
    @Instil("db")
    def post(self, service: SwapDB):
        # Get limited JWT and 2FA code from request
        code: int | None = int(request.form.get("code"))

        # Check if limited JWT and 2FA code are present, if not return 400
        if not code:
            return {"message": "Bad Request"}, 400

        """
        # Decode limited JWT to get user ID and check expiry time
        payload = limited_jwt.split(".")[1]

        # Make sure payload is padded correctly
        if len(payload) % 4 != 0:
            payload += "=" * (4 - len(payload) % 4)
        payload = base64.b64decode(payload)
        payload = json.loads(payload)
        user_id: int = int(payload["sub"])
        expiry_time = payload["exp"]
        """

        # NOTE: Validate that this works and remove above section
        jwt: JwtValidator | None = get_jwt()

        if jwt is None:
            return {"message": "Unauthorized"}, 401

        payload: dict[str, ALLOWED_CLAIM_DATA] = jwt.get_payload()

        try:
            user_id: int = int(payload["sub"])
            expiry: int = int(payload["exp"])
        except KeyError:
            return {"message": "Unauthorized"}, 401

        # If expiry time is less than current time, return unauthorized
        if int(expiry) < int(time()):
            return {"message": "Unauthorized"}, 401

        # Get user secret from database
        user_secret: str | None = UserTable.get_totp_secret(service, user_id)

        # If user secret is not found, return unauthorized
        if not user_secret:
            return {"message": "Unauthorized"}, 401

        # Logic to verify 2FA code and generate full access JWT
        if int(totp(user_secret)) != code:
            return {"message": "Unauthorized"}, 401

        # Set expiry time for full access JWT
        expiry_time: int = int(time()) + JWT_ACCESS_EXP

        # Produce new JWT with full access
        full_access_jwt: str = (
            Jwt(JWT_ACCESS_KEY)
            .add_claim("iss", "elearn-backend")
            .add_claim("aud", "elearn-access")
            .add_claim("sub", f"{user_id}")
            .add_claim("exp", f"{expiry_time}")
            .sign()
        )

        # Return full access JWT
        return {
            "message": "Verification successful",
            "full_access_jwt": full_access_jwt,
        }, 200
