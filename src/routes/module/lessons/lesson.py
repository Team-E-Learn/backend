from flask import request
from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from backend.database.blocks import BlocksTable
from backend.database.lessons import LessonsTable

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen



class Lesson(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.PUT,
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
                SwagParam(
                    "sections",
                    "formData",
                    "string",
                    True,
                    "The sections of the lesson",
                    "{'section1': ['content1', 'content2'], 'section2': ['content3', 'content4']}",
                ),
            ],
            [SwagResp(200, "Lesson created")],
        )
    )
    @Instil("db")
    def put(self, service: Connection[TupleRow]):
        lesson_id = request.form.get("lesson_id")
        module_id = request.form.get("module_id")
        title = request.form.get("title")
        sections = request.form.get("sections")

        # create new lesson using module_id, title, and sections
        LessonsTable.create_lesson(service, lesson_id, module_id, title, sections)
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
    def delete(self, service: Connection[TupleRow]):
        lesson_id = request.form.get("lesson_id")

        # delete lesson using lesson_id
        if LessonsTable.delete_lesson(service, lesson_id):
            return {"message": "Lesson deleted"}, 200
        else:
            return {"message": "Lesson not found"}, 404
