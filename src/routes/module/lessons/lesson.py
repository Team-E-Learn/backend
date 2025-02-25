from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from backend.database.blocks import BlocksTable

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

    # get lesson sidebar with basic blocks using lesson_id
    @Instil("db")
    def get(self, lesson_id: int, conn: Connection[TupleRow]):
        blocks = []
        for block in BlocksTable.get_blocks(conn, lesson_id):
            block_type, block_order, data = block
            blocks.append({
                "block_type": block_type,
                "block_order": block_order,
                "data": data
            })
        return {"blocks": blocks}

