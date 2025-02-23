from psycopg.connection import Connection
from psycopg.rows import TupleRow


class DashboardTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS dashboard (
        userID INT REFERENCES users(userID) NOT NULL,
        widgetID VARCHAR(48) NOT NULL,
        widgetType VARCHAR(48) NOT NULL,
        x INT NOT NULL,
        y INT NOT NULL
    );"""
        )