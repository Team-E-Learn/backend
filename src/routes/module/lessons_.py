from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class Lessons(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Lesson"],
            "Returns a list of openable lessons",
            [],
            [SwagResp(200, "Returns the list of lessons")],
        )
    )
    # todo convert to use DB not dummy data
    @Instil("db")
    def get(self, service: Connection[TupleRow]) -> dict:
        # Demo return data
        return {
            "lessons": [
                {
                    "id": "lesson_1",
                    "title": "Introduction to Python",
                    "description": "Learn the basics of Python programming.",
                    "url": "https://example.com/lessons/1"
                },
                {
                    "id": "lesson_2",
                    "title": "Advanced Python",
                    "description": "Dive deeper into Python programming concepts.",
                    "url": "https://example.com/lessons/2"
                },
                {
                    "id": "lesson_3",
                    "title": "Python for Data Science",
                    "description": "Learn how to use Python for data science.",
                    "url": "https://example.com/lessons/3"
                }
            ]
        }