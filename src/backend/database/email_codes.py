from typing import Any

from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement


class EmailCodesTable:

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS email_codes (
        email VARCHAR(48) PRIMARY KEY UNIQUE NOT NULL,
        code VARCHAR(48) NOT NULL
    );"""
            )
        )

    @staticmethod
    def add_code(conn: SwapDB, email: str, code: str) -> None:
        cursor: SwapCursor = conn.get_cursor()
        _ = cursor.execute(
            StringStatement("INSERT INTO email_codes (email, code) VALUES (%s, %s)"),
            (email, code),
        )

    @staticmethod
    def get_code(conn: SwapDB, email: str) -> str | None:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT code FROM email_codes WHERE email = %s"), (email,)
        )
        tup_res: tuple[Any, ...] | None = result.fetch_one()

        return None if tup_res is None else tup_res[0]
