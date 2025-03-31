from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement


class ModuleCodesTable:
    """Manages database operations for module activation codes.


    This class provides methods to create the module_codes table and manage
    activation codes for educational modules. The codes can be used to activate
    specific modules or sets of modules for users.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        cursor = conn.get_cursor()
        cursor.execute(StringStatement("""
            CREATE TABLE IF NOT EXISTS module_codes (
                code_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
                code CHAR(6) UNIQUE NOT NULL,
                module_ids INTEGER[] NOT NULL DEFAULT '{}'
            );
        """))

    @staticmethod
    def write_code(conn: SwapDB, code: str, module_ids: list[int]) -> None:
        cursor = conn.get_cursor()

        # Insert or update code
        cursor.execute(
            StringStatement(
                """
                INSERT INTO module_codes (code, module_ids)
                VALUES (%s, %s)
                ON CONFLICT (code)
                DO UPDATE SET module_ids = EXCLUDED.module_ids
                RETURNING code_id
                """
            ),
            (code, module_ids)
        )

    @staticmethod
    def write_codes(conn: SwapDB) -> None:
        # Get all module IDs
        cursor = conn.get_cursor()
        result = cursor.execute(StringStatement("SELECT moduleID FROM modules ORDER BY moduleID"))
        all_modules = [row[0] for row in result.fetch_all()]

        # Create codes with different module selections
        codes = [
            ("INTRO1", all_modules[:3]),
            ("ADVMOD", all_modules[3:6] if len(all_modules) > 3 else []),
            ("ALLMOD", all_modules)
        ]

        # Write codes to the database
        for code, modules in codes:
            ModuleCodesTable.write_code(conn, code, modules)

    @staticmethod
    def get_code_modules(conn: SwapDB, code: str) -> SwapResult:
        cursor = conn.get_cursor()
        result = cursor.execute(
            StringStatement("SELECT module_ids FROM module_codes WHERE code = %s"), (code,)
        )
        return result.fetch_one()[0]
