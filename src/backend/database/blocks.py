import json
from typing import Any

from psycopg.connection import Connection
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
        blocks = [
            (1, 1, '2038473', 1, {"question_content": "what is the colour of the sky?", "question_answer": "blue"}),
            (1, 2, '03848293', 2, {"text": "The sky is blue"}),
            (1, 3, '2038473', 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (1, 4, '2038473', 4, {"image_url": "https://www.example.com/image.jpg"}),
            (2, 1, '2038473', 1, {"question_content": "what is the colour of the grass?", "question_answer": "green"}),
            (2, 2, '03848293', 2, {"text": "The grass is green"}),
            (2, 3, '2038473', 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (2, 4, '2038473', 4, {"image_url": "https://www.example.com/image.jpg"}),
            (3, 1, '2038473', 1, {"question_content": "what is the colour of the sea?", "question_answer": "blue"}),
            (3, 2, '03848293', 2, {"text": "The sea is blue"}),
            (3, 3, '2038473', 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (3, 4, '2038473', 4, {"image_url": "https://www.example.com/image.jpg"}),
            (4, 1, '2038473', 1, {"question_content": "what is the colour of the sun?", "question_answer": "yellow"}),
            (4, 2, '03848293', 2, {"text": "The sun is yellow"}),
            (4, 3, '2038473', 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (4, 4, '2038473', 4, {"image_url": "https://www.example.com/image.jpg"})
        ]

        cursor = conn.cursor()
        for lesson_id, block_type, block_id, order, data in blocks:
            if isinstance(data, dict):
                data = json.dumps(data)
            cursor.execute(
                "INSERT INTO blocks (lessonID, blockType, blockOrder, data) VALUES (%s, %s, %s, %s)",
                (lesson_id, block_type, order, data)
            )

    @staticmethod
    def get_blocks(service: Connection[TupleRow], lesson_id: int) -> dict:
        cursor = service.cursor()
        cursor.execute("SELECT blockType, blockOrder, data FROM blocks WHERE lessonID = %s", (lesson_id,))
        rows = cursor.fetchall()
        blocks = []
        for row in rows:
            block_type, block_order, data = row
            if isinstance(data, str):
                data = json.loads(data)
            blocks.append({
                "block_type": block_type,
                "block_order": block_order,
                "data": data
            })
        return {"blocks": blocks}