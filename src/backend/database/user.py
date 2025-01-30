from psycopg.connection import Connection
from psycopg.rows import TupleRow


class UserTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS users (
        userID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        accountType VARCHAR(16) NOT NULL,
        firstName VARCHAR(48) NOT NULL,
        lastName VARCHAR(48) NOT NULL,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );"""
        )

    @staticmethod
    def get_by_username(conn: Connection[TupleRow], username: str):
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username = %s;", (username,))
        return cursor.fetchone()

    @staticmethod
    def get_by_email(conn: Connection[TupleRow], email: str):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        return cursor.fetchone()