from flask import request
from flask_restful import Resource
from backend.auth import get_jwt_sub
from backend.database.lessons import LessonsTable
from backend.database.modules import ModulesTable
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
                    "module_id",
                    "formData",
                    "number",
                    True,
                    "The module id of the lesson",
                    "1",
                ),
                SwagParam(
                    "lesson_id",
                    "formData",
                    "number",
                    True,
                    "The lesson id for the lesson",
                    "1",
                ),
                SwagParam(
                    "title",
                    "formData",
                    "string",
                    True,
                    "The title of the lesson",
                    "example_title",
                )
            ],
            [SwagResp(200, "Lesson created"), SwagResp(404, "Lesson not found")],
            protected=True
        )
    )
    @Instil("db")
    def post(self, service: SwapDB):
        # Get lesson data from request
        try:
            lesson_id = int(request.form.get("lesson_id", -1))
            module_id = int(request.form.get("module_id", -1))
        except TypeError:
            return {"error": "Failed to validate type of the lesson and module id"}, 400

        if lesson_id == -1 or module_id == -1:
            return {"error": "You must supply a lesson id and module id"}, 400

        if (sub := get_jwt_sub()) is None:
            return {"message": "Unauthorized"}, 401

        if not ModulesTable.module_owned_by_user(service, module_id, sub):
            return {"message": "Unauthorized"}, 401

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
                    "module_id",
                    "formData",
                    "integer",
                    True,
                    "The module id of the lesson",
                    "1",
                ),
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
            protected=True
        )
    )
    @Instil("db")
    def delete(self, service: SwapDB):
        # Get module_id and lesson_id from request
        module_id = int(request.form.get("module_id", 0))
        lesson_id = int(request.form.get("lesson_id", 0))

        if (sub := get_jwt_sub()) is None:
            return {"message": "Unauthorized"}, 401

        if not LessonsTable.user_can_delete(service, lesson_id, sub):
            return {"message": "Unauthorized"}, 401

        # Delete lesson using module_id and lesson_id, if successful return a 200 response
        if LessonsTable.delete_lesson(service, module_id, lesson_id):
            return {"message": "Lesson deleted"}, 200
        # If fails, return a 404 response
        else:
            return {"message": "Lesson not found"}, 404
