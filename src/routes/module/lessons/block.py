from flask import request
from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from backend.database.blocks import BlocksTable

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen

class Block(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.PUT,
            ["Block"],
            "Creates a new block",
            [
                SwagParam(
                    "lesson_id",
                    "path",
                    "number",
                    True,
                    "The lesson id of the block",
                    "1",
                ),
                SwagParam(
                    "block_type",
                    "formData",
                    "number",
                    True,
                    "The type of block",
                    "1",
                ),
                SwagParam(
                    "order",
                    "formData",
                    "number",
                    True,
                    "The order of the block",
                    "1",
                ),
                SwagParam(
                    "data",
                    "formData",
                    "object",
                    True,
                    "The data of the block",
                    "{}",
                ),
            ],
            [SwagResp(200, "Block created")],
        )
    )
    @Instil("db")
    def put(self, lesson_id: int, service: Connection[TupleRow]):
        block_type: str | None = request.form.get("block_type")
        order: str | None = request.form.get("order")
        data: str | None = request.form.get("data")

        if BlocksTable.write_block(service, lesson_id, block_type, order, data):
            return {"message": "Block created"}, 200
        else:
            return {"message": "Block not created, invalid lesson ID"}, 400

    @SwagGen(
        SwagDoc(
            SwagMethod.DELETE,
            ["Block"],
            "Deletes a block",
            [
                SwagParam(
                    "lesson_id",
                    "path",
                    "number",
                    True,
                    "The lesson id of the block",
                    "1",
                ),
                SwagParam(
                    "block_type",
                    "formData",
                    "number",
                    True,
                    "The type of block",
                    "1",
                ),
                SwagParam(
                    "order",
                    "formData",
                    "number",
                    True,
                    "The order of the block",
                    "1",
                ),
            ],
            [SwagResp(200, "Block deleted")],
        )
    )
    @Instil("db")
    def delete(self, lesson_id: int, service: Connection[TupleRow]):
        block_type: str | None = request.form.get("block_type")
        order: str | None = request.form.get("order")

        if BlocksTable.delete_block(service, lesson_id, block_type, order):
            return {"message": "Block deleted"}, 200
        else:
            return {"message": "Block not found"}, 404

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Block"],
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
