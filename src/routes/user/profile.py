"""
"get": {
                "tags": ["User"],
                "summary": "Returns the profile information for a specific user",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "type": "int",
                        "required": True,
                        "description": "The user id to get the profile information for",
                        "default": "1234"
                    }
                ],
                "responses": {"200": {"description": "Returns the profile information"}}
            }
"""
