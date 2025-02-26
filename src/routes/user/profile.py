from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from backend.database.user import UserTable

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Profile(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["User"],
            "Returns the profile information for a specific user",
            [
                SwagParam(
                    "user_id",
                    "path",
                    "integer",
                    True,
                    "The user id to add to the module",
                    "1",
                )
            ],
            [SwagResp(200, "Returns the profile information")],
        )
    )

    # get user profile information using user_id
    @Instil("db")
    def get(self, user_id: int, service: Connection[TupleRow]):
        user = UserTable.get_user_profile(service, user_id)
        if user is None:
            return {"error": "User not found"}  # Guard clause for user not found
        return {
            "username": user[0],
            "email": user[1],
            "firstName": user[2],
            "lastName": user[3],
            "accountType": user[4],
        }
