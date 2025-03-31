from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
"""
Module for managing email verification codes in the database.
Provides operations for creating, storing, retrieving, and validating email verification codes.
"""


class EmailCodesTable:
    """Manages database operations for the email_codes table.

    This class provides methods to create the email_codes table and manage
    verification codes used in the email verification process. Each record
    contains an email, its associated verification code, and a verification status.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS email_codes (
        email VARCHAR(48) PRIMARY KEY UNIQUE NOT NULL,
        code VARCHAR(48) NOT NULL,
        verified BOOLEAN DEFAULT FALSE
    );"""
            )
        )

    @staticmethod
    def add_code(conn: SwapDB, email: str, code: str) -> None:
        cursor: SwapCursor = conn.get_cursor()
        cursor.execute(
            StringStatement("INSERT INTO email_codes (email, code) VALUES (%s, %s)"),
            (email, code),
        )

    @staticmethod
    def get_code(conn: SwapDB, email: str) -> str | None:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT code FROM email_codes WHERE email = %s"), (email,)
        )
        tup_res: tuple[str] | None = result.fetch_one()

        return None if tup_res is None else tup_res[0]

    @staticmethod
    def set_verified(conn: SwapDB, email: str) -> None:
        cursor: SwapCursor = conn.get_cursor()
        cursor.execute(
            StringStatement("UPDATE email_codes SET verified = TRUE WHERE email = %s"),
            (email,),
        )
