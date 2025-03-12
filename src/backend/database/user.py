from psycopg.connection import Connection
from psycopg.cursor import Cursor
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
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(256) NOT NULL,
        totpSecret VARCHAR(16) NOT NULL
    );"""
        )

    @staticmethod
    def get_by_username(conn: Connection[TupleRow], username: str):
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(f"SELECT * FROM users WHERE username = %s;", (username,))
        return cursor.fetchone()

    @staticmethod
    def get_by_email(conn: Connection[TupleRow], email: str):
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        return cursor.fetchone()

    # this populates user_ids 1-4 with dummy data
    # no alternative API call to add users, so this is the only way to add them
    @staticmethod
    def write_users(conn: Connection[TupleRow]) -> None:
        # format is (accountType, firstName, lastName, username, email)
        users: list[tuple[str, str, str, str, str, str]] = [
            (
                "user",
                "Alice",
                "Smith",
                "alice.smith",
                "alice.smith@example.com",
                "example_password",
            ),
            (
                "admin",
                "Bob",
                "Johnson",
                "bob.johnson",
                "bob.johnson@example.com",
                "example_password",
            ),
            (
                "user",
                "Carol",
                "Williams",
                "carol.williams",
                "carol.williams@example.com",
                "example_password",
            ),
            (
                "admin",
                "David",
                "Brown",
                "david.brown",
                "david.brown@example.com",
                "example_password",
            ),
        ]

        cursor: Cursor[TupleRow] = conn.cursor()
        for accountType, firstName, lastName, username, email, password in users:
            _ = cursor.execute(
                "SELECT 1 FROM users WHERE username = %s OR email = %s",
                (username, email),
            )

            if cursor.fetchone() is not None:
                continue

            _ = cursor.execute(
                "INSERT INTO users (accountType, firstName, lastName, username, email, password) "
                + "VALUES (%s, %s, %s, %s, %s, %s)",
                (accountType, firstName, lastName, username, email, password),
            )

    # this function is called from src/routes/user/profile.py
    @staticmethod
    def get_user_profile(
        conn: Connection[TupleRow], user_id: int
    ) -> tuple[str, str, str, str, str] | None:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(
            "SELECT username, email, firstName, lastName, accountType FROM users WHERE userID = %s",
            (user_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def user_exists(conn: Connection[TupleRow], user_id: int) -> bool:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute("SELECT 1 FROM users WHERE userID = %s", (user_id,))
        return cursor.fetchone() is not None
