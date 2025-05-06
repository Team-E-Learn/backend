from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement

"""
Module for managing educational lessons in the database.
Provides operations for creating, populating, retrieving, and deleting lessons
associated with educational modules.
"""


class LessonsTable:
    """Manages database operations for the lessons table.

    This class provides methods to create the lessons table and manage lesson data
    for modules.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS lessons (
        lessonID INT NOT NULL,
        moduleID INT NOT NULL,
        title VARCHAR(48) NOT NULL,
        PRIMARY KEY (lessonID, moduleID),
        FOREIGN KEY (moduleID) REFERENCES modules(moduleID)
    );
            """
            )
        )

    @staticmethod
    def create_lesson(
        conn: SwapDB,
        lesson_id: int,
        module_id: int,
        title: str,
    ) -> None:
        cursor: SwapCursor = conn.get_cursor()
        cursor.execute(
            StringStatement(
                "INSERT INTO lessons (lessonID, moduleID, title) VALUES (%s, %s, %s) "
                + "ON CONFLICT (lessonID, moduleID) DO UPDATE SET "
                + "title = EXCLUDED.title"
            ),
            (lesson_id, module_id, title),
        )
        conn.commit()

    # For http://127.0.0.1:5000/v1/module/5/lessons
    @staticmethod
    def write_lessons(conn: SwapDB) -> None:
        # Format is (lesson_id, module_id, title)
        lessons: list[tuple[int, int, str]] = [
            (1, 1, "Introduction"),
            (2, 1, "Lesson 1"),
            (3, 1, "Lesson 2"),
            (4, 1, "Lesson 3"),
            (1, 2, "Introduction"),
            (2, 2, "Lesson 1"),
            (3, 2, "Lesson 2"),
            (4, 2, "Lesson 3"),
            (5, 3, "Introduction"),
            (1, 3, "Lesson 1"),
            (2, 3, "Lesson 2"),
            (3, 3, "Lesson 3"),
            (1, 4, "Introduction"),
            (2, 4, "Lesson 1"),
            (3, 4, "Lesson 2"),
            (4, 4, "Lesson 3"),
        ]

        # Write sample lessons to the database
        cursor: SwapCursor = conn.get_cursor()
        for lesson_id, module_id, title in lessons:
            cursor.execute(
                StringStatement(
                    "INSERT INTO lessons (lessonID, moduleID, title) VALUES (%s, %s, %s) "
                    + "ON CONFLICT (lessonID, moduleID) DO UPDATE SET "
                    + "title = EXCLUDED.title"
                ),
                (lesson_id, module_id, title),
            )
        conn.commit()

    @staticmethod
    def delete_lesson(conn: SwapDB, module_id:int, lesson_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()

        # Check if lesson exists
        if not cursor.execute(
                StringStatement("SELECT * FROM lessons WHERE lessonID = %s AND moduleID = %s"), (lesson_id, module_id)
        ).fetch_one():
            # If lesson does not exist, return False
            return False

        # If lesson exists, delete blocks associated with lesson
        cursor.execute(
            StringStatement("DELETE FROM blocks WHERE lessonID = %s AND moduleID = %s"), (lesson_id, module_id)
        )

        # Then delete lesson and return True
        cursor.execute(
            StringStatement("DELETE FROM lessons WHERE lessonID = %s AND moduleID = %s"), (lesson_id, module_id)
        )
        conn.commit()
        return True

    @staticmethod
    def get_lessons(conn: SwapDB, module_id: int) -> list[tuple[int, int, str]]:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT * FROM lessons WHERE moduleID = %s"), (module_id,)
        )
        tuple_res: list[tuple[int, int, str]] | None = result.fetch_all()

        if tuple_res is None:
            return []

        return tuple_res

    @staticmethod
    def user_can_delete(conn: SwapDB, lesson_id: int, user_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("""
                    SELECT 1
                    FROM lessons
                    JOIN modules ON modules.moduleid = lessons.moduleid
                    JOIN organisations ON organisations.orgid = modules.orgid
                    WHERE lessons.lessonid = %s AND ownerid = %s
            """),
            (lesson_id, user_id),
        )
        return result.fetch_one() is not None
