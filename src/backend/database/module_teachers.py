from psycopg.connection import Connection
from psycopg.rows import TupleRow


class ModuleTeachersTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS module_teachers (
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        userID INT REFERENCES users(userID) NOT NULL,
        PRIMARY KEY (moduleID, userID)
    );"""
        )
