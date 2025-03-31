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
            "Adds a module to a user",
            [
                SwagParam(
                    "org_id",
                    "path",
                    "integer",
                    True,
                    "The org id that the module is from",
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
            [
                SwagResp(200, "Module added to user"),
                SwagResp(403, "Organization does not own the module"),
                SwagResp(404, "User, Organization, or Module not found"),
                SwagResp(500, "Server error")
            ],
        )
    )
    @Instil("db")
    def put(self, org_id: int, module_id: int, user_id: int, service: SwapDB
    ) -> tuple[dict[str, str | bool], int]:
        # Add a module to a user using org_id, module_id and user_id
        # Check user_id exists in the users table
        if not UserTable.user_exists(service, user_id):
            return {"success": False, "error": "User not found"}, 404

        # Check org_id exists
        if not OrganisationsTable.org_exists(service, org_id):
            return {"success": False, "error": "Organisation not found"}, 404

        # Check module_id exists
        if not ModulesTable.module_exists(service, module_id):
            return {"success": False, "error": "Module not found"}, 404

        # Check org owns module
        if not ModulesTable.module_owned_by_org(service, module_id, org_id):
            return {"success": False, "error": "Organisation does not own the module"}, 403

        # Insert into subscriptions user_id and module_id
        try:
            SubscriptionsTable.add_subscription(service, user_id, module_id)
        except Exception as e:
            # Return error if exception is raised
            return {"success": False, "error": str(e)}, 500

        # If subscription is added without error, return success message
        return {"success": True, "message": "Successfully added subscription to user"}, 200
