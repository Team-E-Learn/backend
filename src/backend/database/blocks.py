from json import dumps

from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement

"""
Module for managing lesson blocks in the database.
Provides CRUD operations for the blocks table which stores different types of content blocks.
"""


class BlocksTable:
    """Manages database operations for the blocks table.

    This class provides methods to create the blocks table and perform
    CRUD operations on block records. Blocks are the content units within lessons.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS blocks (
        blockID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        lessonID INT REFERENCES lessons(lessonID) NOT NULL,
        blockType INT NOT NULL,
        blockOrder INT NOT NULL,
        data JSON NOT NULL,
        UNIQUE (lessonID, blockType, blockOrder)
    );"""
            )
        )

    @staticmethod
    def write_block(
        conn: SwapDB, lesson_id: int, block_type: int, order: int, data: dict[str, str]
    ) -> bool:
        cursor: SwapCursor = conn.get_cursor()

        # Verify the lesson exists before adding a block to it
        if not cursor.execute(
            StringStatement("SELECT 1 FROM lessons WHERE lessonID = %s"), (lesson_id,)
        ).fetch_one():
            return False

        # Convert data dictionary to JSON string
        data_json: str = dumps(data)

        # Insert block into blocks table
        _ = cursor.execute(
            StringStatement(
                """
            INSERT INTO blocks (lessonID, blockType, blockOrder, data)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (lessonID, blockType, blockOrder)
            DO UPDATE SET data = EXCLUDED.data
            """
            ),
            (lesson_id, block_type, order, data_json),
        )
        return True

    # For http://127.0.0.1:5000/v1/module/lesson/
    @staticmethod
    def write_blocks(conn: SwapDB) -> None:
        # Format is (lesson_id, block_type, order (of appearance on page), data)
        blocks: list[tuple[int, int, int, dict[str, str]]] = [
            (
                1,
                1,
                1,
                {
                    "question_content": "what is the colour of the sky?",
                    "question_answer": "blue",
                },
            ),
            (1, 2, 2, {"text": "The sky is blue"}),
            (1, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (1, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
            (
                2,
                1,
                1,
                {
                    "question_content": "what is the colour of the grass?",
                    "question_answer": "green",
                },
            ),
            (2, 2, 2, {"text": "The grass is green"}),
            (2, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (2, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
            (
                3,
                1,
                1,
                {
                    "question_content": "what is the colour of the sea?",
                    "question_answer": "blue",
                },
            ),
            (3, 2, 2, {"text": "The sea is blue"}),
            (3, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (3, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
            (
                4,
                1,
                1,
                {
                    "question_content": "what is the colour of the sun?",
                    "question_answer": "yellow",
                },
            ),
            (4, 2, 2, {"text": "The sun is yellow"}),
            (4, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (4, 4, 4, {"image_url": "https://www.example.com/image.jpg"}),
        ]

        cursor: SwapCursor = conn.get_cursor()
        for lesson_id, block_type, order, data in blocks:
            data = dumps(data)
            _ = cursor.execute(
                StringStatement(
                    "INSERT INTO blocks (lessonID, blockType, blockOrder, data) VALUES (%s, %s, %s, %s)"
                ),
                (lesson_id, block_type, order, data),
            )

    @staticmethod
    def delete_block(conn: SwapDB, lesson_id: int, block_type: int, order: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()

        # Check if block exists
        if not cursor.execute(
            StringStatement(
                "SELECT * FROM blocks WHERE lessonID = %s AND blockType = %s AND blockOrder = %s"
            ),
            (lesson_id, block_type, order),
        ).fetch_one():
            # If block does not exist, return False
            return False

        # If block exists, delete it, then return True
        _ = cursor.execute(
            StringStatement(
                "DELETE FROM blocks WHERE lessonID = %s AND blockType = %s AND blockOrder = %s"
            ),
            (lesson_id, block_type, order),
        )
        return True

    @staticmethod
    def get_blocks(conn: SwapDB, lesson_id: int) -> list[tuple[int, int, str]]:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement(
                "SELECT blockType, blockOrder, data FROM blocks WHERE lessonID = %s"
            ),
            (lesson_id,),
        )
        tup: list[tuple[int, int, str]] | None = result.fetch_all()
        if tup is None:
            return []
        return tup
