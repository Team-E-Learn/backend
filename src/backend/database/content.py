from psycopg.connection import Connection
from psycopg.rows import TupleRow


class ContentTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS content (
        contentID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        title VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        content JSON NOT NULL
    );"""
        )
        conn.commit()
