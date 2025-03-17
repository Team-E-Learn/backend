from flask_restful import Resource
from backend.database.user import UserTable
from backend.database.organisations import OrganisationsTable
from backend.database.modules import ModulesTable
from backend.database.subscriptions import SubscriptionsTable

from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
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
                    "1",
                ),
                SwagParam(
                    "module_id",
                    "path",
                    "integer",
                    True,
                    "The module id to add the user to",
                    "1",
                ),
                SwagParam(
                    "user_id",
                    "path",
                    "integer",
                    True,
                    "The user id to add to the module",
                    "1",
                ),
            ],
            [SwagResp(200, "Module added to user")],
        )
    )
    @Instil("db")
    def put(
        self, org_id: int, module_id: int, user_id: int, service: SwapDB 
    ) -> dict[str, str | bool]:
        # add a module to a user using org_id, module_id and user_id
        # check user_id exists in the users table
        if not UserTable.user_exists(service, user_id):
            return {"success": False, "error": "User not found"}

        # check org_id exists
        if not OrganisationsTable.org_exists(service, org_id):
            return {"success": False, "error": "Organisation not found"}

        # check module_id exists
        if not ModulesTable.module_exists(service, module_id):
            return {"success": False, "error": "Module not found"}

        # check org owns module
        if not ModulesTable.module_owned_by_org(service, module_id, org_id):
            return {"success": False, "error": "Organisation does not own the module"}

        # insert into subscriptions user_id and module_id
        try:
            if not SubscriptionsTable.add_subscription(service, user_id, module_id):
                return {"success": False, "error": "Failed to add subscription"}
        except Exception as e:
            return {"success": False, "error": str(e)}

        return {"success": True, "message": "Successfully added subscription to user"}
