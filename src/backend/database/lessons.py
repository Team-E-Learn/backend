from psycopg.connection import Connection
from psycopg.rows import TupleRow


class LessonsTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS lessons (
        lessonID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        title VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL
    );"""
        )

    # for http://127.0.0.1:5000/v1/module/5/lessons
    # no alternative API call to add lessons, so this is the only way to add them
    @staticmethod
    def write_lessons(conn: Connection[TupleRow]) -> None:
        # format is (module_id, title, description)
        lessons = [
            (1, 'Introduction', 'An introduction to the module'),
            (1, 'Lesson 1', 'The first lesson in the module'),
            (1, 'Lesson 2', 'The second lesson in the module'),
            (1, 'Lesson 3', 'The third lesson in the module'),
            (2, 'Introduction', 'An introduction to the module'),
            (2, 'Lesson 1', 'The first lesson in the module'),
            (2, 'Lesson 2', 'The second lesson in the module'),
            (2, 'Lesson 3', 'The third lesson in the module'),
            (3, 'Introduction', 'An introduction to the module'),
            (3, 'Lesson 1', 'The first lesson in the module'),
            (3, 'Lesson 2', 'The second lesson in the module'),
            (3, 'Lesson 3', 'The third lesson in the module'),
            (4, 'Introduction', 'An introduction to the module'),
            (4, 'Lesson 1', 'The first lesson in the module'),
            (4, 'Lesson 2', 'The second lesson in the module'),
            (4, 'Lesson 3', 'The third lesson in the module')
        ]

        cursor = conn.cursor()
        for module_id, title, description in lessons:
            cursor.execute(
                "INSERT INTO lessons (moduleID, title, description) VALUES (%s, %s, %s)",
                (module_id, title, description)
            )


    @staticmethod
    def get_lessons(conn: Connection[TupleRow], module_id: int) -> list[tuple[int, int, str, str]]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM lessons WHERE moduleID = %s",
            (module_id,)
        )
        return cursor.fetchall()
