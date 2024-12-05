from flask_restful import Resource

from lib.swagdoc.swagdoc import SwagDoc, SwagParam, SwagMethod, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class User(Resource):

    @SwagGen(
        SwagDoc(
            "/v1/org/<org_id>/module/<module_id>/user/<user_id>",
            SwagMethod.PUT,
            ["Module"],
            "Adds a bundle or module to a user",
            [
                SwagParam(
                    "org_id",
                    "path",
                    "int",
                    True,
                    "The org id to add the module to",
                    "1234",
                ),
                SwagParam(
                    "module_id",
                    "path",
                    "int",
                    True,
                    "The module id to add the user to",
                    "1234",
                ),
                SwagParam(
                    "user_id",
                    "path",
                    "int",
                    True,
                    "The user id to add to the module",
                    "1234",
                ),
            ],
            [SwagResp(200, "Module added to user")],
        )
    )
    def put(self, org_id: int, mod_id: int, user_id: int) -> dict[str, bool]:
        return {"success": True}
