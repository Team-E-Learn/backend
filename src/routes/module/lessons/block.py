from flask import request
from flask_restful import Resource, reqparse
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
            ["Lesson"],
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
        block_type = request.form.get("block_type")
        order = request.form.get("order")
        data = request.form.get("data")

        BlocksTable.write_block(service, lesson_id, block_type, order, data)
        return {"message": "Block created"}, 200

    @SwagGen(
        SwagDoc(
            SwagMethod.DELETE,
            ["Lesson"],
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
        block_type = request.form.get("block_type")
        order = request.form.get("order")

        if BlocksTable.delete_block(service, lesson_id, block_type, order):
            return {"message": "Block deleted"}, 200
        else:
            return {"message": "Block not found"}, 404
