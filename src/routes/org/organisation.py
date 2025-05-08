import ast
from flask import request
from flask_restful import Resource
from typing import Any
from backend.auth import valid_jwt_sub
from backend.database.organisations import OrganisationsTable
from backend.database.modules import ModulesTable
from backend.database.bundles import BundlesTable
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
                    "bundles",
                    "formData",
                    "string",
                    False,
                    "List of bundles with modules to create for this Organisation",
                    "[{'bundle_name': 'Bundle 1', 'modules': [{'name': 'Module 1'}, {'name': 'Module 2'}]}]",
                ),
                SwagParam(
                    "modules",
                    "formData",
                    "string",
                    True,
                    "list of standalone modules to create for this Organisation",
                    "[{'name': 'Module 1'}, {'name': 'Module 2'}]",
                ),
                SwagParam(
                    "owner_id",
                    "formData",
                    "number",
                    True,
                    "The ID of the owner of the Organisation",
                    2,
                ),
            ],
            [
                SwagResp(200, "Organisation created successfully"),
                SwagResp(400, "Invalid request data"),
            ],
            protected=True
        )
    )
    @Instil("db")
    def post(self, service: SwapDB) -> tuple[dict[str, Any], int]:
        # Get Organisation data from request
        name: str | None = request.form.get("name")
        owner_id_str: str | None = request.form.get("owner_id")

        if owner_id_str is None:
            return {"message": "Owner ID is required"}, 400

        try:
            owner_id: int = int(owner_id_str)
        except ValueError:
            return {"message": "Owner ID is required"}, 400
        
        if not valid_jwt_sub(owner_id):
            return {"message": "You are unauthorised to access this endpoint"}, 401

        # Parse bundles and modules lists
        try:
            bundles_str: str | None = request.form.get("bundles", "[]")
            bundles: list[dict[str, Any]] = ast.literal_eval(bundles_str)
        except (SyntaxError, ValueError):
            return {"message": "Invalid bundles format"}, 400
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

        # Create/Update Organisation
        org_id: int | None = OrganisationsTable.write_org(
            service, name, owner_id
        )

        # Process bundles and their modules
        created_bundles: list[dict[str, Any]] = []
        for bundle in bundles:
            if not isinstance(bundle, dict) or "bundle_name" not in bundle:
               return {"message": "Invalid bundle format"}, 400

            bundle_name: str = bundle["bundle_name"]

            # Create a bundle
            bundle_id: int | None = BundlesTable.write_bundle(service, org_id, bundle_name)

            # Process modules in this bundle
            bundle_modules: list[dict[str, Any]] = bundle.get("modules", [])
            created_modules: list[dict[str, Any]] = []

            for module in bundle_modules:
                if not isinstance(module, dict) or "name" not in module:
                    continue

                module_name: str = module["name"]

                # Create module
                module_id: int | None = ModulesTable.write_module(service, org_id, module_name)

                if module_id:
                    # Associate module with a bundle
                    BundlesTable.associate_module(service, bundle_id, module_id)
                    created_modules.append({
                        "name": module_name,
                        "module_id": module_id
                    })

            created_bundles.append({
                "bundle_id": bundle_id,
                "bundle_name": bundle_name,
                "modules": created_modules
            })

        # Process direct modules (not in bundles)
        created_direct_modules: list[dict[str, Any]] = []
        for module in modules:
            if not isinstance(module, dict) or "name" not in module:
                return {"message": "Invalid module format"}, 400

            module_name: str = module.get("name", "Blank Name")

            # Overwriting happens automatically in the database
            module_id: int | None = ModulesTable.write_module(service, org_id, module_name)

            if module_id:
                created_direct_modules.append({
                    "id": module_id,
                    "name": module_name
                })

        # Return success response with org_id and created modules
        return {
            "message": "Organisation created successfully",
            "Organisation": {
                "name": name,
                "id": org_id,
                "bundles": created_bundles,
                "modules": created_direct_modules
            },
        }, 200
