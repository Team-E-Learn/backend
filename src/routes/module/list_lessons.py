from flask_restful import Resource
from backend.auth import get_jwt_sub
from backend.database.lessons import LessonsTable
from backend.database.subscriptions import SubscriptionsTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Lessons(Resource):
    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Lesson"],
            "Returns a list of lessons for a specific module",
            [
                SwagParam(
                    "module_id",
                    "path",
                    "integer",
                    True,
                    "The module id to retrieve the lessons for",
                    "1",
                )
            ],
            [SwagResp(200, "Returns the lessons")],
            protected=True
        )
    )
    # Get list of lessons for a specific module using module_id
    @Instil("db")
    def get(self, module_id: int, service: SwapDB):
        if (user_id := get_jwt_sub()) is None:
            return {"message": "You are unauthorised to access this endpoint"}, 401

        if not SubscriptionsTable.is_member(service, user_id, module_id):
            return {"message": "You are unauthorised to access this endpoint"}, 401

        lessons: list[tuple[int, int, str]] = LessonsTable.get_lessons(
            service, module_id
        )

        return {"lessons": [{"id": row[0], "title": row[2]} for row in lessons]}, 200
