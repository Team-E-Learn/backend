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

    # get list of lessons for a specific module using module_id
    @Instil("db")
    def get(self, module_id: int, service: Connection[TupleRow]):
        lessons = LessonsTable.get_lessons(service, module_id)
        return {
            "lessons": [
                {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2]
                }
                for row in lessons
            ]
        }