from flask import request
from flask_restful import Resource
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen
from backend.database.user import UserTable

class CheckUsername(Resource):
    def __init__(self, conn):
        self.conn = conn

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
            [SwagResp(200, "Username exists"), SwagResp(400, "Bad Request"), SwagResp(404, "Username not found")],
        )
    )
    def get(self):
        username = request.args.get('username')

        # Check if username exists
        if UserTable.get_by_username(self.conn, username):
            return {"message": "Username exists"}, 200
        else:
            return {"message": "Valid username"}, 200