from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class ModuleDashboard(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["User"],
            "Returns the module dashboard for a specific user and module",
            [
                SwagParam(
                    "user_id",
                    "path",
                    "integer",
                    True,
                    "The user id to retrieve the module dashboard for",
                    "1",
                ),
                SwagParam(
                    "module_id",
                    "path",
                    "integer",
                    True,
                    "The module id to retrieve the dashboard for",
                    "1",
                )
            ],
            [SwagResp(200, "Returns the module dashboard")],
        )
    )
    @Instil("db")
    def get(self, user_id: int, module_id: int, service: Connection[TupleRow]) -> dict:
        with service.cursor() as cur:
            cur.execute(
                "SELECT * FROM module_dashboard WHERE userID = %s AND moduleID = %s",
                (user_id, module_id)
            )
            dashboard = cur.fetchall()

            return {
                "elements": [
                    {
                        "id": row[2],
                        "type": row[3],
                        "position": {"x": row[4], "y": row[5]}
                    }
                    for row in dashboard
                ]
            }