"""
Module for managing educational lessons in the database.
Provides operations for creating, populating, retrieving, and deleting lessons
associated with educational modules.
"""
import json
from psycopg import Cursor
from psycopg.connection import Connection
from psycopg.rows import TupleRow


class LessonsTable:
    """Manages database operations for the lessons table.

    This class provides methods to create the lessons table and manage lesson data
    for modules. Each lesson has a title and JSON-structured content
    organized into sections.
    """

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS lessons (
        lessonID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        title VARCHAR(48) NOT NULL,
        sections JSON NOT NULL
    );"""
        )

    @staticmethod
    def create_lesson(conn: Connection[TupleRow], lesson_id: int, module_id: int,
                      title: str, sections: dict[str, str]) -> None:
        sections = json.dumps(sections)
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(
            "INSERT INTO lessons (lessonID, moduleID, title, sections) VALUES (%s, %s, %s, %s) "
            "ON CONFLICT (lessonID) DO UPDATE SET title = EXCLUDED.title, sections = EXCLUDED.sections",
            (lesson_id, module_id, title, sections)
        )

    # For http://127.0.0.1:5000/v1/module/5/lessons
    @staticmethod
    def write_lessons(conn: Connection[TupleRow]) -> None:
        # Format is (module_id, title, sections)
        lessons: list[tuple[int, str, str]] = [
            (1, 'Introduction', '{"content": "Welcome to the introduction"}'),
            (1, 'Lesson 1', '{"content": "This is lesson 1"}'),
            (1, 'Lesson 2', '{"content": "This is lesson 2"}'),
            (1, 'Lesson 3', '{"content": "This is lesson 3"}'),
            (2, 'Introduction', '{"content": "Welcome to the introduction"}'),
            (2, 'Lesson 1', '{"content": "This is lesson 1"}'),
            (2, 'Lesson 2', '{"content": "This is lesson 2"}'),
            (2, 'Lesson 3', '{"content": "This is lesson 3"}'),
            (3, 'Introduction', '{"content": "Welcome to the introduction"}'),
            (3, 'Lesson 1', '{"content": "This is lesson 1"}'),
            (3, 'Lesson 2', '{"content": "This is lesson 2"}'),
            (3, 'Lesson 3', '{"content": "This is lesson 3"}'),
            (4, 'Introduction', '{"content": "Welcome to the introduction"}'),
            (4, 'Lesson 1', '{"content": "This is lesson 1"}'),
            (4, 'Lesson 2', '{"content": "This is lesson 2"}'),
            (4, 'Lesson 3', '{"content": "This is lesson 3"}'),
        ]

        # Write sample lessons to the database
        cursor: Cursor[TupleRow] = conn.cursor()
        for module_id, title, sections in lessons:
            _ = cursor.execute(
                "INSERT INTO lessons (moduleID, title, sections) VALUES (%s, %s, %s)",
                (module_id, title, sections)
            )

    @staticmethod
    def delete_lesson(conn: Connection[TupleRow], lesson_id: int) -> bool:
        cursor: Cursor[TupleRow] = conn.cursor()

        # Check if lesson exists
        if not cursor.execute("SELECT * FROM lessons WHERE lessonID = %s", (lesson_id,)).fetchone():
            # If lesson does not exist, return False
            return False

        # If lesson exists, delete blocks associated with lesson
        _ = cursor.execute("DELETE FROM blocks WHERE lessonID = %s", (lesson_id,))

        # Then delete lesson and return True
        _ = cursor.execute("DELETE FROM lessons WHERE lessonID = %s", (lesson_id,))
        conn.commit()
        return True


    @staticmethod
    def get_lessons(conn: Connection[TupleRow], module_id: int) -> list[tuple[int, int, str, str]]:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(
            "SELECT * FROM lessons WHERE moduleID = %s",
            (module_id,)
        )
        return cursor.fetchall()
