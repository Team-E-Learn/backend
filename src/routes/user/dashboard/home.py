from flask_restful import Resource, reqparse
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class HomeDashboard(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["User"],
            "Returns the home dashboard for a specific user",
            [
                SwagParam(
                    "user_id",
                    "query",
                    "integer",
                    True,
                    "The user id to add to the module",
                    "1234",
                )
            ],
            [SwagResp(200, "Returns the home dashboard")],
        )
    )
    @Instil("db")
    def get(self, service: Connection[TupleRow]) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, location='args')
        args = parser.parse_args()

        user_id = args['user_id']

        # Demo return data
        return {
            "elements": [
                {
                    "id": "announcements_widget",
                    "type": "announcements",
                    "position": {"x": 10, "y": 20}
                },
                {
                    "id": "grade_centre_widget",
                    "type": "grade_centre",
                    "position": {"x": 30, "y": 20}
                },
                {
                    "id": "calendar_widget",
                    "type": "calendar",
                    "position": {"x": 10, "y": 40}
                }
            ]
        }