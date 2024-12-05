from flask_restful import Resource

from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Profile(Resource):

    @SwagGen(
        SwagDoc(
            "/v1/user/<user_id>/profile",
            SwagMethod.GET,
            ["User"],
            "Returns the profile information for a specific user",
            [
                SwagParam(
                    "user_id",
                    "path",
                    "int",
                    True,
                    "The user id to add to the module",
                    "1234",
                )
            ],
            [SwagResp(200, "Returns the profile information")],
        )
    )
    def get(self, user_id: int):
        return {"username": "bob"}




