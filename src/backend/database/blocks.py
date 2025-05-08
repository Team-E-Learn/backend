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
            (1, 1, 1, 1, "text block", {"title": "Lorem Ipsum", "text": "Lorem ipsum dolor sit amet"}),
            (1, 2, 2, 2, "image block", {"image": "image", "altText": "Bliss location, Sonoma Valley in 2006"}),
            (1, 3, 3, 3, "text and image block",
                {"title": "Lorem Ipsum", "text": "Lorem ipsum dolor sit amet",
                 "image": "image", "altText": "Bliss location, Sonoma Valley in 2006"}),
            (1, 4, 4, 4, "download block", {"downloadLink": "https://www.google.com", "fileName": "document.docx"}),
            (1, 5, 5, 5, "quiz block", {"question": "press option A",
                                        "options": {
                                        "A": {"text": "Option A", "isCorrect": True},
                                        "B": {"text": "Option B", "isCorrect": False},
                                        "C": {"text": "Option C", "isCorrect": False},
                                        "D": {"text": "Option D", "isCorrect": False}}}),

            (2, 2, 2, 2, "text block", {"title": "Lorem Ipsum", "text": "Lorem ipsum dolor sit amet"}),
            (2, 3, 3, 3, "image block", {"image": "image", "altText": "Bliss location, Sonoma Valley in 2006"}),
            (2, 4, 4, 4, "download block", {"downloadLink": "https://www.google.com", "fileName": "document.docx"}),

            (3, 1, 1, 1, "text block", {"title": "Lorem Ipsum", "text": "Lorem ipsum dolor sit amet"}),
            (3, 2, 2, 2, "download block", {"downloadLink": "https://www.google.com", "fileName": "document.docx"}),
            (3, 3, 3, 3, "text block", {"title": "Lorem Ipsum", "text": "Lorem ipsum dolor sit amet"}),
            (3, 4, 4, 4, "download block", {"downloadLink": "https://www.google.com", "fileName": "document.docx"}),

            (4, 1, 1, 1, "text block", {"title": "Lorem Ipsum", "text": "Lorem ipsum dolor sit amet"}),
            (4, 2, 2, 2, "image block", {"image": "image", "altText": "Bliss location, Sonoma Valley in 2006"}),
            (4, 3, 3, 3, "download block", {"downloadLink": "https://www.google.com", "fileName": "document.docx"}),
            (4, 4, 4, 4, "text block", {"title": "Lorem Ipsum", "text": "Lorem ipsum dolor sit amet"}),
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

