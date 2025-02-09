from flask_restful import Resource, reqparse
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class CourseDashboard(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["User"],
            "Returns the course dashboard for a specific user and course",
            [
                SwagParam(
                    "user_id",
                    "query",
                    "integer",
                    True,
                    "The user id to retrieve the course dashboard for",
                    "1234",
                ),
                SwagParam(
                    "course_id",
                    "query",
                    "integer",
                    True,
                    "The course id to retrieve the dashboard for",
                    "5678",
                )
            ],
            [SwagResp(200, "Returns the course dashboard")],
        )
    )
    @Instil("db")
    def get(self, service: Connection[TupleRow]) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, location='args')
        parser.add_argument('course_id', type=int, required=True, location='args')
        args = parser.parse_args()

        user_id = args['user_id']
        course_id = args['course_id']

        # Demo return data
        return {
            "elements": [
                {
                    "id": "announcements_widget",
                    "type": "announcements",
                    "position": {"x": 10, "y": 20}
                },
                {
                    "id": "info_widget",
                    "type": "info",
                    "position": {"x": 30, "y": 20}
                },
                {
                    "id": "about_widget",
                    "type": "about",
                    "position": {"x": 10, "y": 40}
                },
                {
                    "id": "grade_centre_widget",
                    "type": "grade_centre",
                    "position": {"x": 30, "y": 40}
                },
                {
                    "id": "calendar_widget",
                    "type": "calendar",
                    "position": {"x": 10, "y": 60}
                }
            ]
        }