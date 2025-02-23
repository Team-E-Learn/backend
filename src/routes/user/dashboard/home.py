from flask_restful import Resource
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
                    "path",
                    "integer",
                    True,
                    "The user id to add to the module",
                    "1",
                )
            ],
            [SwagResp(200, "Returns the home dashboard")],
        )
    )
    @Instil("db")
    def get(self, user_id: int, service: Connection[TupleRow]) -> dict:
       with service.cursor() as cur:
            cur.execute(
                "SELECT * FROM dashboard WHERE userID = %s",
                (user_id,)
            )
            dashboard = cur.fetchall()

            return {
                "elements": [
                    {
                        "id": row[1],
                        "type": row[2],
                        "position": {"x": row[3], "y": row[4]}
                    }
                    for row in dashboard
                ]
            }
