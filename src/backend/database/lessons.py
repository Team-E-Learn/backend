from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement


class LessonsTable:

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS lessons (
        lessonID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        title VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL
    );"""
            )
        )

    # for http://127.0.0.1:5000/v1/module/5/lessons
    # no alternative API call to add lessons, so this is the only way to add them
    @staticmethod
    def write_lessons(conn: SwapDB) -> None:
        # format is (module_id, title, description)
        lessons: list[tuple[int, str, str]] = [
            (1, "Introduction", "An introduction to the module"),
            (1, "Lesson 1", "The first lesson in the module"),
            (1, "Lesson 2", "The second lesson in the module"),
            (1, "Lesson 3", "The third lesson in the module"),
            (2, "Introduction", "An introduction to the module"),
            (2, "Lesson 1", "The first lesson in the module"),
            (2, "Lesson 2", "The second lesson in the module"),
            (2, "Lesson 3", "The third lesson in the module"),
            (3, "Introduction", "An introduction to the module"),
            (3, "Lesson 1", "The first lesson in the module"),
            (3, "Lesson 2", "The second lesson in the module"),
            (3, "Lesson 3", "The third lesson in the module"),
            (4, "Introduction", "An introduction to the module"),
            (4, "Lesson 1", "The first lesson in the module"),
            (4, "Lesson 2", "The second lesson in the module"),
            (4, "Lesson 3", "The third lesson in the module"),
        ]

        cursor: SwapCursor = conn.get_cursor()
        for module_id, title, description in lessons:
            _ = cursor.execute(
                StringStatement(
                    "INSERT INTO lessons (moduleID, title, description) VALUES (%s, %s, %s)"
                ),
                (module_id, title, description),
            )

    @staticmethod
    def get_lessons(conn: SwapDB, module_id: int) -> list[tuple[int, int, str, str]]:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT * FROM lessons WHERE moduleID = %s"), (module_id,)
        )
        tuple_res: list[tuple[int, int, str, str]] | None = result.fetch_all()

        if tuple_res is None:
            return []

        return tuple_res
