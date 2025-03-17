from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement


class UserTable:

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS users (
        userID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        accountType VARCHAR(16) NOT NULL,
        firstName VARCHAR(48) NOT NULL,
        lastName VARCHAR(48) NOT NULL,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(256) NOT NULL
    );"""
            )
        )

    @staticmethod
    def get_by_username(conn: SwapDB, username: str):
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT * FROM users WHERE username = %s;"), (username,)
        )
        return result.fetch_one()

    @staticmethod
    def get_by_email(conn: SwapDB, email: str):
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT * FROM users WHERE email = %s;"), (email,)
        )
        return result.fetch_one()

    # this populates user_ids 1-4 with dummy data
    # no alternative API call to add users, so this is the only way to add them
    @staticmethod
    def write_users(conn: SwapDB) -> None:
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

        cursor: SwapCursor = conn.get_cursor()
        for accountType, firstName, lastName, username, email, password in users:
            result: SwapResult = cursor.execute(
                StringStatement(
                    "SELECT 1 FROM users WHERE username = %s OR email = %s"
                ),
                (username, email),
            )

            if result.fetch_one() is not None:
                continue

            _ = cursor.execute(
                StringStatement(
                    "INSERT INTO users (accountType, firstName, lastName, username, email, password) "
                    + "VALUES (%s, %s, %s, %s, %s, %s)"
                ),
                (accountType, firstName, lastName, username, email, password),
            )

    # this function is called from src/routes/user/profile.py
    @staticmethod
    def get_user_profile(
        conn: SwapDB, user_id: int
    ) -> tuple[str, str, str, str, str] | None:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement(
                "SELECT username, email, firstName, lastName, accountType FROM users WHERE userID = %s"
            ),
            (user_id,),
        )
        return result.fetch_one()

    @staticmethod
    def user_exists(conn: SwapDB, user_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT 1 FROM users WHERE userID = %s"), (user_id,)
        )
        return result.fetch_one() is not None
