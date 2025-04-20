from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
from json import dumps as json_dumps

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
        conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS blocks (
        blockID INT NOT NULL,
        lessonID INT REFERENCES lessons(lessonID) NOT NULL,
        blockType INT NOT NULL,
        blockOrder INT NOT NULL,
        blockName VARCHAR(64) NOT NULL,
        data JSON NOT NULL,
        UNIQUE (lessonID, blockID, blockOrder),
        PRIMARY KEY (lessonID, blockID)
    );"""
            )
        )

    @staticmethod
    def write_block(
        conn: SwapDB, block_id: int, lesson_id: int, block_type: int, order: int, block_name: str, data: dict
    ) -> bool:
        cursor: SwapCursor = conn.get_cursor()

        # Verify the lesson exists before adding a block to it
        if not cursor.execute(
            StringStatement("SELECT 1 FROM lessons WHERE lessonID = %s"), (lesson_id,)
        ).fetch_one():
            return False

        # Convert data dictionary to JSON string
        data_json: str = json_dumps(data)

        # Insert/update block into blocks table
        cursor.execute(
            StringStatement(
                """
            INSERT INTO blocks (blockID, lessonID, blockType, blockOrder, blockName, data)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (lessonID, blockID)
            DO UPDATE SET blockType = EXCLUDED.blockType, blockOrder = EXCLUDED.blockOrder,
                blockName = EXCLUDED.blockName, data = EXCLUDED.data
            """
            ),
            (block_id, lesson_id, block_type, order, block_name, data_json),
        )
        return True

    # For http://127.0.0.1:5000/v1/module/lesson/
    @staticmethod
    def write_blocks(conn: SwapDB) -> None:
        # format: lesson_id, block_id, block_type, order, block_name, data
        blocks: list[tuple[int, int, int, int, str, dict]] = [
            (
                1,
                1,
                1,
                1,
                "Sky Question",
                {
                    "question_content": "what is the colour of the sky?",
                    "question_answer": "blue",
                },
            ),
            (1, 2, 2, 2, "Sky Text", {"text": "The sky is blue"}),
            (1, 3, 3, 3, "Sky Video", {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (1, 4, 4, 4, "Sky Image", {"image_url": "https://www.example.com/image.jpg"}),
            (
                2,
                1,
                1,
                1,
                "Grass Question",
                {
                    "question_content": "what is the colour of the grass?",
                    "question_answer": "green",
                },
            ),
            (2, 2, 2, 2, "Grass Text", {"text": "The grass is green"}),
            (2, 3, 3, 3, "Grass Video", {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (2, 4, 4, 4, "Grass Image", {"image_url": "https://www.example.com/image.jpg"}),
            (
                3,
                1,
                1,
                1,
                "Sea Question",
                {
                    "question_content": "what is the colour of the sea?",
                    "question_answer": "blue",
                },
            ),
            (3, 2, 2, 2, "Sea Text", {"text": "The sea is blue"}),
            (3, 3, 3, 3, "Sea Video", {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (3, 4, 4, 4, "Sea Image", {"image_url": "https://www.example.com/image.jpg"}),
            (
                4,
                1,
                1,
                1,
                "Sun Question",
                {
                    "question_content": "what is the colour of the sun?",
                    "question_answer": "yellow",
                },
            ),
            (4, 2, 2, 2, "Sun Text", {"text": "The sun is yellow"}),
            (4, 3, 3, 3, "Sun Video", {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
            (4, 4, 4, 4, "Sun Image", {"image_url": "https://www.example.com/image.jpg"}),
        ]

        # Write sample block data to the blocks table
        cursor: SwapCursor = conn.get_cursor()
        for lesson_id, block_id, block_type, order, block_name, data in blocks:
            data_json: str = json_dumps(data)
            cursor.execute(
                StringStatement(
                    "INSERT INTO blocks (lessonID, blockID, blockType, blockOrder, blockName, data) "
                    "VALUES (%s, %s, %s, %s, %s, %s) "
                ),
                (lesson_id, block_id, block_type, order, block_name, data_json),
            )

    @staticmethod
    def delete_block(conn: SwapDB, lesson_id: int, block_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()

        # Check if block exists
        if not cursor.execute(
            StringStatement(
                "SELECT * FROM blocks WHERE lessonID = %s AND blockID = %s"
            ),
            (lesson_id, block_id),
        ).fetch_one():
            # If block does not exist, return False
            return False

        # If block exists, delete it, then return True
        cursor.execute(
            StringStatement(
                "DELETE FROM blocks WHERE lessonID = %s AND blockID = %s"
            ),
            (lesson_id, block_id),
        )
        return True

    @staticmethod
    def get_blocks(conn: SwapDB, lesson_id: int) -> list[tuple[int, int, int, str, dict]]:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement(
                "SELECT blockType, blockID, blockOrder, blockName, data FROM blocks WHERE lessonID = %s"
            ),
            (lesson_id,),
        )
        tup: list[tuple[int, int, int, str, dict]] | None = result.fetch_all()
        if tup is None:
            return []
        return tup
