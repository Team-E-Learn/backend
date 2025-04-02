from flask import request
from flask_restful import Resource
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from backend.database.user import UserTable


class CheckUsername(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Auth"],
            "Checks if a username exists",
            [
                SwagParam(
                    "username",
                    "query",
                    "string",
                    True,
                    "The username to check",
                    "example_username",
                ),
            ],
            [
                SwagResp(200, "Username exists"),
                SwagResp(400, "Bad Request"),
            ],
        )
    )
    @Instil("db")
    def get(self, service: SwapDB):
        username: str | None = request.args.get("username")

        # Check if username, if not return 400
        if not username:
            return {"message": "Bad Request"}, 400

        # Check if username exists
        if UserTable.get_by_username(service, username):
            return {"message": "Username exists"}, 200

        # Return 200 on valid username
        return {"message": "Valid username"}, 200
