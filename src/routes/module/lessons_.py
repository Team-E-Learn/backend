from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from backend.database.lessons import LessonsTable

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
        )
    )

    @Instil("db")
    def get(self, module_id: int, service: Connection[TupleRow]) -> dict:
        return LessonsTable.get_lessons(service, module_id)