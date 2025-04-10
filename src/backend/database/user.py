from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
from werkzeug.security import generate_password_hash
"""
Module for managing user accounts in the database.
Provides operations for creating, authenticating, retrieving and validating user accounts
that can own organizations, access modules, and track educational progress.
"""


class UserTable:
    """Manages database operations for the users table.

    This class provides methods to create the users table and manage user account data.
    Each user has an account type (user/teacher), personal information, authentication
    credentials, and a TOTP secret for two-factor authentication. Users represent the
    primary actors in the system who interact with educational content.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        conn.get_cursor().execute(
            StringStatement(
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

    # This populates user_ids 1-4 with dummy data
    # No alternative API call to add users, so this is the only way to add them
    @staticmethod
    def write_users(conn: SwapDB) -> None:
        # Format is (accountType, firstName, lastName, username, email)
        users: list[tuple[str, str, str, str, str, str, str]] = [
            (
                "user",
                "Alice",
                "Smith",
                "alice.smith",
                "alice.smith@example.com",
                generate_password_hash("example_password"),
                "WVTBSKRNKORNCBMI",
            ),
            (
                "teacher",
                "Bob",
                "Johnson",
                "bob.johnson",
                "bob.johnson@example.com",
                generate_password_hash("example_password"),
                "KEQWOVVUJDIFQSJD",
            ),
            (
                "user",
                "Carol",
                "Williams",
                "carol.williams",
                "carol.williams@example.com",
                generate_password_hash("example_password"),
                "HARAUJMIXYGDSRLA",
            ),
            (
                "teacher",
                "David",
                "Brown",
                "david.brown",
                "david.brown@example.com",
                generate_password_hash("example_password"),
                "OSQBCMPVGVZTUGPO",
            ),
        ]

        cursor: SwapCursor = conn.get_cursor()
        for (
            account_type,
            firstName,
            lastName,
            username,
            email,
            password,
            totp_secret,
        ) in users:
            result: SwapResult = cursor.execute(
                StringStatement(
                    "SELECT 1 FROM users WHERE username = %s OR email = %s"
                ),
                (username, email),
            )

            if result.fetch_one() is not None:
                continue

            # Insert user into the database
            cursor.execute(
                StringStatement(
                    "INSERT INTO users (accountType, firstName, lastName, username, email, password, totpSecret) "
                    + "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                ),
                (
                    account_type,
                    firstName,
                    lastName,
                    username,
                    email,
                    password,
                    totp_secret,
                ),
            )

    # This function is called from src/routes/user/profile.py
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

    @staticmethod
    def get_totp_secret(conn: SwapDB, user_id: int) -> str | None:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT totpSecret FROM users WHERE userID = %s"),
            (user_id,),
        )
        result_tup: tuple[str] | None = result.fetch_one()
        return None if result_tup is None else result_tup[0]
