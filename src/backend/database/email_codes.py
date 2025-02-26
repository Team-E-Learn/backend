from psycopg.cursor import Cursor
from psycopg.connection import Connection
from psycopg.rows import TupleRow


class EmailCodesTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS email_codes (
        email VARCHAR(48) PRIMARY KEY UNIQUE NOT NULL,
        code VARCHAR(48) NOT NULL
    );"""
        )

    @staticmethod
    def add_code(conn: Connection[TupleRow], email: str, code: str) -> None:
        print(email, code)
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(
            "INSERT INTO email_codes (email, code) VALUES (%s, %s)", (email, code)
        )

    @staticmethod
    def get_code(conn: Connection[TupleRow], email: str) -> str | None:
        print(email)
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute("SELECT code FROM email_codes WHERE email = %s", (email,))
        result: TupleRow | None = cursor.fetchone()

        return None if result is None else result[0]
