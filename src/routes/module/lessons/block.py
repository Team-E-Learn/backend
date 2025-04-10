import ast
from flask import request
from flask_restful import Resource
from backend.database.blocks import BlocksTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Block(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
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
                    "block_name",
                    "formData",
                    "string",
                    True,
                    "The name of the block",
                    "Block Name",
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
            [SwagResp(200, "Block created"), SwagResp(400, "Block not created")],
        )
    )
    @Instil("db")
    def post(self, lesson_id: int, service: SwapDB):
        # Get block data from request and convert to appropriate types
        block_type = int(request.form.get("block_type", 0))
        order = int(request.form.get("order", 0))
        block_name = str(request.form.get("block_name", 0))
        data = ast.literal_eval(request.form.get("data"))

        # Try to create a block, if successful return a 200 response
        if BlocksTable.write_block(service, lesson_id, block_type, order, block_name, data):
            return {"message": "Block created"}, 200
        # If fails, return a 400 response
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
            [SwagResp(200, "Block deleted"), SwagResp(404, "Block not found")],
        )
    )
    @Instil("db")
    def delete(self, lesson_id: int, service: SwapDB):
        # Get block data from request and convert to integers
        block_type: int = int(request.form.get("block_type", 0))
        order: int = int(request.form.get("order", 0))

        # Try to delete a block, if successful return a 200 response
        if BlocksTable.delete_block(service, lesson_id, block_type, order):
            return {"message": "Block deleted"}, 200
        # If fails, return a 404 response
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
    def get(self, lesson_id: int, service: SwapDB):
        # Get lesson sidebar with basic blocks using lesson_id
        blocks: list[dict[str, int | str]] = []
        for block_type, block_order, block_name, data in BlocksTable.get_blocks(service, lesson_id):
            blocks.append(
                {"block_type": block_type, "block_order": block_order, "block_name": block_name, "data": data}
            )
        return {"blocks": blocks}, 200