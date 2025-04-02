from flask_restful import Resource
from backend.database.dashboard import DashboardTable
from lib.dataswap.database import SwapDB
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
    def get(self, user_id: int, service: SwapDB):
        # Get home dashboard for a specific user using user_id
        dashboard: list[tuple[int, str, str, int, int]] = DashboardTable.get_dashboard(
            service, user_id
        )
        return {
            "elements": [
                {"id": row[1], "type": row[2], "position": {"x": row[3], "y": row[4]}}
                for row in dashboard
            ]
        }, 200
