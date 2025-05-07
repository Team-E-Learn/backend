from flask_restful import Resource
from backend.database.user import UserTable
from lib.dataswap.database import SwapDB
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
                    "The user id to get information about",
                    "1",
                )
            ],
            [SwagResp(200, "Returns the profile information")],
            protected=True
        )
    )
    # get user profile information using user_id
    @Instil("db")
    def get(self, user_id: int, service: SwapDB):
        # Get user profile information using user_id
        user = UserTable.get_user_profile(service, user_id)

        # Guard clause for if user not found
        if user is None:
            return {"error": "User not found"}

        return {
            "username": user[0],
            "email": user[1],
            "firstName": user[2],
            "lastName": user[3],
            "accountType": user[4],
        }, 200
