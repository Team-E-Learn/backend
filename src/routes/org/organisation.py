import ast
from flask import request
from flask_restful import Resource
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
                    "description",
                    "formData",
                    "string",
                    False,
                    "The description of the Organisation",
                    "An example Organisation description",
                ),
                SwagParam(
                    "modules",
                    "formData",
                    "object",
                    True,
                    "List of modules to create for this Organisation",
                    "[{'name': 'Module 1', 'description': 'Description for module 1'}]",
                ),
            ],
            [
                SwagResp(200, "Organisation created successfully"),
                SwagResp(400, "Invalid request data"),
                SwagResp(409, "Organisation already exists")
            ],
        )
    )
    @Instil("db")
    def post(self, service: SwapDB):
        # Get Organisation data from request
        name = request.form.get("name")
        description = request.form.get("description", "")

        # Parse modules list
        try:
            modules = ast.literal_eval(request.form.get("modules", "[]"))
        except (SyntaxError, ValueError):
            return {"message": "Invalid modules format"}, 400

        # Validate required fields
        if not name:
            return {"message": "Organisation name is required"}, 400

        if not isinstance(modules, list):
            return {"message": "Modules must be a list"}, 400

        # Create Organisation
        org_id = OrganisationsTable.create_Organisation(service, name, description)

        if not org_id:
            return {"message": "Organisation already exists"}, 409

        # Create modules for the Organisation
        created_modules = []
        for module in modules:
            if not isinstance(module, dict) or "name" not in module:
                continue

            module_name = module.get("name")
            module_description = module.get("description", "")

            # Overwriting happens automatically in the database
            module_id = ModulesTable.create_module(
                service,
                org_id,
                module_name,
                module_description
            )

            if module_id:
                created_modules.append({
                    "id": module_id,
                    "name": module_name
                })

        return {
            "message": "Organisation created successfully",
            "Organisation": {
                "id": org_id,
                "name": name
            },
            "modules": created_modules
        }, 200