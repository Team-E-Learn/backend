from flask_restful import Resource

from lib.swagdoc.swagdoc import SwagDoc, SwagParam, SwagMethod, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class User(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.PUT,
            ["Module"],
            "Adds a bundle or module to a user",
            [
                SwagParam(
                    "org_id",
                    "path",
                    "integer",
                    True,
                    "The org id to add the module to",
                    "1234",
                ),
                SwagParam(
                    "module_id",
                    "path",
                    "integer",
                    True,
                    "The module id to add the user to",
                    "1234",
                ),
                SwagParam(
                    "user_id",
                    "path",
                    "integer",
                    True,
                    "The user id to add to the module",
                    "1234",
                ),
            ],
            [SwagResp(200, "Module added to user")],
        )
    )
    def put(self, org_id: int, mod_id: int, user_id: int) -> dict[str, bool]:

        # TODO: Find user via id
        # TODO: Verify org owns mod id
        # TODO: Insert into subscriptions user id and org id

        return {"success": True}


