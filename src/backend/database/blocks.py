import json
from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


class BlocksTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS blocks (
        blockID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        lessonID INT REFERENCES lessons(lessonID) NOT NULL,
        blockType INT NOT NULL,
        blockOrder INT NOT NULL,
        data JSON NOT NULL
    );"""
        )

    # for http://127.0.0.1:5000/v1/module/lesson/5
    # no alternative API call to add blocks, so this is the only way to add them
    @staticmethod
    def write_blocks(conn: Connection[TupleRow]) -> None:
        # format is (lesson_id, block_type, order (of appearance on page), data)
        blocks: list[tuple[int, int, int, dict[str, str]]] = [
            (1, 1, 1,
                {
                    "question_content": "what is the colour of the sky?",
                    "question_answer": "blue",
                },
            ),
            (1, 2, 2, {"text": "The sky is blue"}),
            (1, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (1, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
            (2, 1, 1,
                {
                    "question_content": "what is the colour of the grass?",
                    "question_answer": "green",
                },
            ),
            (2, 2, 2, {"text": "The grass is green"}),
            (2, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (2, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
            (3, 1, 1,
                {
                    "question_content": "what is the colour of the sea?",
                    "question_answer": "blue",
                },
            ),
            (3, 2, 2, {"text": "The sea is blue"}),
            (3, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (3, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
            (4, 1, 1,
                {
                    "question_content": "what is the colour of the sun?",
                    "question_answer": "yellow",
                },
            ),
            (4, 2, 2, {"text": "The sun is yellow"}),
            (4, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (4, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
        ]

        cursor: Cursor[TupleRow] = conn.cursor()
        for lesson_id, block_type, order, data in blocks:
            data = json.dumps(data)
            _ = cursor.execute(
                "INSERT INTO blocks (lessonID, blockType, blockOrder, data) VALUES (%s, %s, %s, %s)",
                (lesson_id, block_type, order, data),
            )

    @staticmethod
    def get_blocks(
        service: Connection[TupleRow], lesson_id: int
    ) -> list[tuple[int, int, str]]:
        cursor: Cursor[TupleRow] = service.cursor()
        _ = cursor.execute(
            "SELECT blockType, blockOrder, data FROM blocks WHERE lessonID = %s",
            (lesson_id,),
        )
        return cursor.fetchall()
