import ast
from flask import request
from flask_restful import Resource
from backend.auth import get_jwt_sub
from backend.database.blocks import BlocksTable
from backend.database.lessons import LessonsTable
from backend.database.modules import ModulesTable
from backend.database.subscriptions import SubscriptionsTable
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
                    "module_id",
                    "formData",
                    "number",
                    True,
                    "The module id of the block",
                    "2",
                ),
                SwagParam(
                    "lesson_id",
                    "path",
                    "number",
                    True,
                    "The lesson id of the block",
                    "2",
                ),
                SwagParam(
                    "block_id",
                    "formData",
                    "number",
                    True,
                    "The block id to create",
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
                    "name",
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
            protected=True,
        )
    )
    @Instil("db")
    def post(self, lesson_id: int, service: SwapDB):
        # Get block data from request and convert to appropriate types
        module_id = int(request.form.get("module_id", 0))
        block_id = int(request.form.get("block_id", 0))
        block_type = int(request.form.get("block_type", 0))
        order = int(request.form.get("order", 0))
        name = str(request.form.get("name", 0))

        if (str_data := request.form.get("data")) is None:
            return {"message": "Block data not found"}, 400
        data = ast.literal_eval(str_data)

        if (sub := get_jwt_sub()) is None:
            return {"message": "Unauthorized"}, 401

        if not LessonsTable.user_can_delete(service, lesson_id, sub):
            return {"message": "Unauthorized"}, 401

        # Try to create a block, if successful return a 200 response
        if BlocksTable.write_block(
            service, block_id, module_id, lesson_id, block_type, order, name, data
        ):
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
                    "module_id",
                    "formData",
                    "number",
                    True,
                    "The module id of the block",
                    "1",
                ),
                SwagParam(
                    "lesson_id",
                    "path",
                    "number",
                    True,
                    "The lesson id of the block",
                    "1",
                ),
                SwagParam(
                    "block_id",
                    "formData",
                    "number",
                    True,
                    "The block id to delete",
                    "1",
                ),
            ],
            [SwagResp(200, "Block deleted"), SwagResp(404, "Block not found")],
            protected=True,
        )
    )
    @Instil("db")
    def delete(self, lesson_id: int, service: SwapDB):
        # Get block data from request and convert to integers
        module_id = int(request.form.get("module_id", 0))
        block_id = int(request.form.get("block_id", 0))

        if (sub := get_jwt_sub()) is None:
            return {"message": "Unauthorized"}, 401

        if not LessonsTable.user_can_delete(service, lesson_id, sub):
            return {"message": "Unauthorized"}, 401

        # Try to delete a block, if successful return a 200 response
        if BlocksTable.delete_block(service, module_id, lesson_id, block_id):
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
                    "module_id",
                    "query",
                    "integer",
                    True,
                    "The module id to retrieve",
                    "9",
                ),
                SwagParam(
                    "lesson_id",
                    "path",
                    "integer",
                    True,
                    "The lesson id to retrieve",
                    "1",
                ),
            ],
            [SwagResp(200, "Returns the lesson sidebar")],
            protected=True,
        )
    )
    @Instil("db")
    def get(self, lesson_id: int, service: SwapDB):
        # Get lesson sidebar with basic blocks using module_id and lesson_id
        module_id = int(request.args.get("module_id", 0))
        blocks: list[dict[str, int | str | dict]] = []

        if (sub := get_jwt_sub()) is None:
            return {"message": "Unauthorized"}, 401

        if not SubscriptionsTable.can_read_lesson(
            service, sub, lesson_id
        ) and not ModulesTable.module_owned_by_user(service, module_id, sub):
            return {"message": "Unauthorized"}, 401

        for (
            block_type,
            block_id,
            block_order,
            block_name,
            data,
        ) in BlocksTable.get_blocks(service, module_id, lesson_id):
            blocks.append(
                {
                    "block_type": block_type,
                    "block_id": block_id,
                    "order": block_order,
                    "name": block_name,
                    "data": data,
                }
            )
            # TODO: implement lesson blocking if not submitted
        return {"blocks": blocks}, 200
