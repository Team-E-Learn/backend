from psycopg.connection import Connection
from psycopg.rows import TupleRow


class ProgressTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS progress (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        progress JSON NOT NULL
    );"""
        )
