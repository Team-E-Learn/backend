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
    @Instil("db")
    def get(self, lesson_id: int, service: Connection[TupleRow]) -> dict:
        # Demo return data
        return {
            "sidebar": {
                "blocks": [
                    {
                        "id": "text_image_block",
                        "type": "text_image",
                        "content": {
                            "text": "Example text",
                            "image_url": "https://example.com/image.png"
                        }
                    },
                    {
                        "id": "video_embed_block",
                        "type": "video_embed",
                        "content": {
                            "video_url": "https://example.com/video.mp4"
                        }
                    },
                    {
                        "id": "simple_game_block",
                        "type": "simple_game",
                        "content": {
                            "game_url": "https://example.com/game"
                        }
                    }
                ]
            }
        }