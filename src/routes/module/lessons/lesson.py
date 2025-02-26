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
    @Instil("db")
    def get(self, lesson_id: int, service: Connection[TupleRow]):
        # get lesson sidebar with basic blocks using lesson_id
        blocks: list[dict[str, int | str]] = []
        for block_type, block_order, data in BlocksTable.get_blocks(service, lesson_id):
            blocks.append(
                {"block_type": block_type, "block_order": block_order, "data": data}
            )
        return {"blocks": blocks}
