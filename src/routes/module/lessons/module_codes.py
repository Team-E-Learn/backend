from flask import request
from flask_restful import Resource
from backend.database.module_codes import ModuleCodesTable
from backend.database.subscriptions import SubscriptionsTable
from backend.database.user import UserTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class ModuleCode(Resource):
    @SwagGen(
        SwagDoc(
            SwagMethod.PUT,
            ["Module"],
            "Activates a module code and subscribes a user to associated modules",
            [
                SwagParam(
                    "user_id",
                    "path",
                    "integer",
                    True,
                    "The ID of the user to subscribe",
                    "1",
                ),
                SwagParam(
                    "code",
                    "formData",
                    "string",
                    True,
                    "The 6-character activation code",
                    "INTRO1",
                ),
            ],
            [
                SwagResp(200, "Successfully subscribed to modules"),
                SwagResp(404, "Code or user not found"),
                SwagResp(400, "Invalid request data"),
            ],
        )
    )
    @Instil("db")
    def put(self, user_id: int, service: SwapDB) -> tuple[dict[str, str | list[int]], int]:
        code: str = request.form.get("code")

        if not user_id:
            return {"message": "User ID is required"}, 400
        if not code:
            return {"message": "Code is required"}, 400
        if len(code) != 6:
            return {"message": "Code must be 6 characters long"}, 404

        # Check user_id exists in the user's table
        if not UserTable.user_exists(service, user_id):
            return {"success": False, "error": "User not found"}, 404

        # Get module IDs for this code
        module_ids: list[int] = ModuleCodesTable.get_code_modules(service, code)
        if not module_ids:
            return {"message": "Code not found"}, 404

        # Subscribe the user to each module individually
        subscribed_modules: list[int] = []
        for module_id in module_ids:
            # Process each module ID individually, not as an array
            SubscriptionsTable.add_subscription(service, user_id, int(module_id))
            subscribed_modules.append(module_id)

        # Return the list of subscribed modules
        return {
            "message": f"Successfully subscribed user {user_id} to {len(subscribed_modules)} modules",
            "modules": subscribed_modules
        }, 200
