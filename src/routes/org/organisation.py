import ast
from flask import request
from flask_restful import Resource
from typing import Any
from backend.database.organisations import OrganisationsTable
from backend.database.modules import ModulesTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Organisation(Resource):
    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Organisation"],
            "Creates a new Organisation with modules",
            [
                SwagParam(
                    "name",
                    "formData",
                    "string",
                    True,
                    "The name of the Organisation",
                    "Example Organisation",
                ),
                SwagParam(
                    "modules",
                    "formData",
                    "string",
                    True,
                    "list of modules to create for this Organisation",
                    "[{'name': 'Module 1'}, {'name': 'Module 2'}]",
                ),
                SwagParam(
                    "owner_id",
                    "formData",
                    "number",
                    True,
                    "The ID of the owner of the Organisation",
                    1,
                ),
            ],
            [
                SwagResp(200, "Organisation created successfully"),
                SwagResp(400, "Invalid request data"),
            ],
        )
    )
    @Instil("db")
    def post(self, service: SwapDB) -> tuple[dict[str, Any], int]:
        # Get Organisation data from request
        name: str | None = request.form.get("name")
        owner_id: int | None = int(request.form.get("owner_id"))

        # Parse modules list
        try:
            modules_str: str | None = request.form.get("modules", "[]")
            modules: list[dict[str, Any]] = ast.literal_eval(modules_str)
        except (SyntaxError, ValueError):
            return {"message": "Invalid modules format"}, 400

        # Validate required fields
        if not name:
            return {"message": "Organisation name is required"}, 400
        if not owner_id:
            return {"message": "Owner ID is required"}, 400
        if not isinstance(modules, list):
            return {"message": "Modules must be a list"}, 400

        # Create/Update Organisation
        org_id: int | None = OrganisationsTable.write_org(service, name, owner_id)

        # Create modules for the Organisation
        created_modules: list[dict[str, Any]] = []
        for module in modules:
            if not isinstance(module, dict) or "name" not in module:
                continue

            module_name: str = module.get("name")

            # Overwriting happens automatically in the database
            module_id: int | None = ModulesTable.write_module(
                service,
                org_id,
                module_name,
            )

            if module_id:
                created_modules.append({
                    "id": module_id,
                    "name": module_name
                })

        # Return success response with org_id and created modules
        return {
            "message": "Organisation created successfully",
            "Organisation": {
                "id": org_id,
                "name": name
            },
            "modules": created_modules
        }, 200
