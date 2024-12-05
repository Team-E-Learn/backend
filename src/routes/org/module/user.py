"""
"/v1/org/<org_id>/module/<module_id>/user/<user_id>": {
            "put": {
                "tags": ["User"],
                "summary": "Adds a bundle or module to a user",
                "parameters": [
                    {
                        "name": "org_id",
                        "in": "path",
                        "type": "int",
                        "required": True,
                        "description": "The org id to add the module to",
                        "default": "1234"
                    },
                    {
                        "name": "module_id",
                        "in": "path",
                        "type": "int",
                        "required": True,
                        "description": "The module id to add to the user",
                        "default": "1234"
                    },
                    {
                        "name": "user_id",
                        "in": "path",
                        "type": "int",
                        "required": True,
                        "description": "The user id to add the module to",
                        "default": "1234"
                    }
                ],
                "responses": {"200": {"description": "Module added to user"}}
            }
        }
"""

from flask_restful import Resource


class User(Resource):
    def put(self, org_id: int, mod_id: int, user_id: int):
        return { "success": True }
