import random

from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class Lesson(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Lesson"],
            "Returns the lesson sidebar with basic blocks",
            [
                SwagParam(
                    "lesson_id",
                    "path",
                    "integer",
                    True,
                    "The lesson id to retrieve",
                    "1",
                )
            ],
            [SwagResp(200, "Returns the lesson sidebar")],
        )
    )
    # todo convert to use DB not dummy data
    @Instil("db")
    def get(self, lesson_id: int, service: Connection[TupleRow]) -> dict:
        # Demo return data
        x = random.randint(1, 3)
        if x == 1:
            return {
                "block_type": "1",
                "block_id": "2038473",
                "order": "1",
                "data": [
                    {
                        "question_content": "what is the colour of the sky?",
                        "question_answer": "blue"
                    },
                    {
                        "question_content": "why is the sea blue",
                        "question_answer": "reflections from the sky"
                    }
                ]
            }
        if x == 2:
            return {
                "block_type": "2",
                "block_id": "03848293",
                "order": "2",
                "data": "iahehfgwi"
            }
        if x == 3:
            return {
                "block_type": "3",
                "block_id": "185454",
                "order": "3",
                "data": "(link to download)"
            }

