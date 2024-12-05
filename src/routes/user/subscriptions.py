from flask_restful import Resource

from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Subscriptions(Resource):
    
    @SwagGen(
        SwagDoc(
            "/v1/user/<user_id>/subscriptions",
            SwagMethod.GET,
            ["User"],
            "Returns the subscribed orgs, bundles and modules for a user",
            [
                SwagParam(
                    "user_id",
                    "path",
                    "int",
                    True,
                    "The user id to add to the module",
                    "1234",
                )
            ],
            [SwagResp(200, "Returns the subscriptions")],
        )
    )
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
