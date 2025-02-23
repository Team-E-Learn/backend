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