"""

"/v1/user/user_id/subscriptions": {
            "get": {
                "tags": ["User info"],
                "summary": "Returns the subscribed orgs, bundles and modules for a specific user",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "type": "string",
                        "required": True,
                        "description": "The user id to get the subscriptions for",
                        "default": "1234"
                    }
                ],
                "responses": {"200": {"description": "Returns the subscriptions"}}
            }
        },
"""

from flask_restful import Resource


class Subscriptions(Resource):
    def get(self, user_id: int):
        return [{
            "org_name": "University of Lincoln",
            "org_id": 1,
            "bundles": [
                {
                    "name": "Computer Science BSc",
                    "modules": [
                        {
                            "name": "Team Software Engineering",
                            "module_id": 1
                        },
                        {
                            "name": "Networking Fundamentals",
                            "module_id": 2
                        },
                        {
                            "name": "Applied Programming Paradigms",
                            "module_id": 3
                        }
                    ]
                }
            ],
            "modules": [
                {
                    "name": "Personal Development",
                    "module_id": 4
                }
            ]
        },
        {
            "org_name": "Microsoft",
            "org_id": 2,
            "bundles": [],
            "modules": [
                {
                    "name": "Excel Certification",
                    "module_id": 5
                }
            ]
        }
    ]
