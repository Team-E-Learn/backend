import ast
from flask import request
from flask_restful import Resource
from backend.database.lessons import LessonsTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Lesson(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.POST,
            ["Lesson"],
            "Creates a new lesson",
            [
                SwagParam(
                    "lesson_id",
                    "formData",
                    "number",
                    True,
                    "The lesson id for the lesson",
                    "1",
                ),
                SwagParam(
                    "module_id",
                    "formData",
                    "number",
                    True,
                    "The module id of the lesson",
                    "1",
                ),
                SwagParam(
                    "title",
                    "formData",
                    "string",
                    True,
                    "The title of the lesson",
                    "example_title",
                ),
            ],
            [SwagResp(200, "Lesson created"), SwagResp(404, "Lesson not found")],
        )
    )
    @Instil("db")
    def post(self, service: SwapDB):
        # Get lesson data from request
        lesson_id = int(request.form.get("lesson_id", 0))
        module_id = int(request.form.get("module_id", 0))
        title = request.form.get("title", "")


        # Create new lesson using module_id, title
        LessonsTable.create_lesson(service, lesson_id, module_id, title)
        return {"message": "Lesson created"}, 200

    @SwagGen(
        SwagDoc(
            SwagMethod.DELETE,
            ["Lesson"],
            "Deletes a lesson",
            [
                SwagParam(
                    "lesson_id",
                    "formData",
                    "integer",
                    True,
                    "The lesson id to delete",
                    "1",
                )
            ],
            [SwagResp(200, "Lesson deleted")],
        )
    )
    @Instil("db")
    def delete(self, service: SwapDB):
        # Get lesson_id from request
        lesson_id = int(request.form.get("lesson_id", 0))

        # Delete lesson using lesson_id, if successful return a 200 response
        if LessonsTable.delete_lesson(service, lesson_id):
            return {"message": "Lesson deleted"}, 200
        # If fails, return a 404 response
        else:
            return {"message": "Lesson not found"}, 404
