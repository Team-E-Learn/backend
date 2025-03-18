"""
Module for managing user accounts in the database.
Provides operations for creating, authenticating, retrieving and validating user accounts
that can own organizations, access modules, and track educational progress.
"""
from werkzeug.security import generate_password_hash
from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


class UserTable:
    """Manages database operations for the users table.

    This class provides methods to create the users table and manage user account data.
    Each user has an account type (user/admin), personal information, authentication
    credentials, and a TOTP secret for two-factor authentication. Users represent the
    primary actors in the system who interact with educational content.
    """

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

    # This populates user_ids 1-4 with dummy data
    # No alternative API call to add users, so this is the only way to add them
    @staticmethod
    def write_users(conn: Connection[TupleRow]) -> None:
        # Format is (accountType, firstName, lastName, username, email)
        users: list[tuple[str, str, str, str, str, str, str]] = [
            (
                "user",
                "Alice",
                "Smith",
                "alice.smith",
                "alice.smith@example.com",
                 generate_password_hash("example_password"),
                "WVTBSKRNKORNCBMI"
            ),
            (
                "admin",
                "Bob",
                "Johnson",
                "bob.johnson",
                "bob.johnson@example.com",
                generate_password_hash("example_password"),
                "KEQWOVVUJDIFQSJD"
            ),
            (
                "user",
                "Carol",
                "Williams",
                "carol.williams",
                "carol.williams@example.com",
                generate_password_hash("example_password"),
                "HARAUJMIXYGDSRLA"
            ),
            (
                "admin",
                "David",
                "Brown",
                "david.brown",
                "david.brown@example.com",
                generate_password_hash("example_password"),
                "OSQBCMPVGVZTUGPO"
            ),
        ]

        # Write sample users to the database
        cursor: Cursor[TupleRow] = conn.cursor()
        for accountType, firstName, lastName, username, email, password, totpSecret in users:
            _ = cursor.execute(
                "SELECT 1 FROM users WHERE username = %s OR email = %s",
                (username, email),
            )

            # Skip if user already exists
            if cursor.fetchone() is not None:
                continue

            # Insert user into the database
            _ = cursor.execute(
                "INSERT INTO users (accountType, firstName, lastName, username, email, password, totpSecret) "
                + "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (accountType, firstName, lastName, username, email, password, totpSecret),
            )

    # This function is called from src/routes/user/profile.py
    @staticmethod
    def get_user_profile(conn: Connection[TupleRow], user_id: int
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

    @staticmethod
    def get_totp_secret(conn: Connection[TupleRow], user_id: int) -> str:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute("SELECT totpSecret FROM users WHERE userID = %s", (user_id,))
        return cursor.fetchone()[0]
