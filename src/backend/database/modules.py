from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement

"""
Module for managing modules in the database.
Provides operations for creating, populating, and validating modules
that are owned by organisations and contain lessons and other content.
"""


class ModulesTable:
    """Manages database operations for the modules table.

    This class provides methods to create the modules table and manage modules
    within the system. Each module has a name, and belongs to an organisation.
    Modules serve as containers for lessons and other content.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS modules (
        moduleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );"""
            )
        )

    @staticmethod
    def write_module(conn: SwapDB, org_id: int, name: str) -> int:
        cursor: SwapCursor = conn.get_cursor()

        # Insert new module
        result = cursor.execute(
            StringStatement(
                "INSERT INTO modules (name, orgID) VALUES (%s, %s) RETURNING moduleID"
            ),
            (name, org_id),
        )

        # Return the moduleID of the newly created module
        return result.fetch_one()[0]

    # Adds 8 modules to the DB, 4 are owned by org_id 1, 2 are owned by org_id 2, 2 are owned by org_id 3
    # No alternative API call to add modules, so this is the only way to add them
    @staticmethod
    def write_modules(conn: SwapDB) -> None:
        # format is (name, orgID)
        modules: list[tuple[str, int]] = [
            ("Personal Development", 1),
            ("Team Software Engineering", 1),
            ("Networking Fundamentals", 1),
            ("Applied Programming Paradigms", 1),
            ("Excel Certification", 2),
            ("Advanced Excel", 2),
            ("Data Analysis", 3),
            ("Machine Learning", 3),
        ]

        cursor: SwapCursor = conn.get_cursor()
        # Write sample modules to the database
        for name, orgID in modules:
            result: SwapResult = cursor.execute(
                StringStatement("SELECT 1 FROM modules WHERE name = %s"), (name,)
            )

            if result.fetch_one() is not None:
                # If the module already exists, skip it
                continue

            # Otherwise, add the module to the database
            _ = cursor.execute(
                StringStatement(
                    "INSERT INTO modules (name, orgID) VALUES (%s, %s)"
                ),
                (name, orgID),
            )

    @staticmethod
    def module_exists(conn: SwapDB, module_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT 1 FROM modules WHERE moduleID = %s"), (module_id,)
        )
        return result.fetch_one() is not None

    @staticmethod
    def module_owned_by_org(conn: SwapDB, module_id: int, org_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT 1 FROM modules WHERE moduleID = %s AND orgID = %s"),
            (module_id, org_id),
        )
        return result.fetch_one() is not None

    @staticmethod
    def module_owned_by_user(conn: SwapDB, module_id: int, user_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("""
                    SELECT 1
                    FROM modules
                    JOIN organisations as org ON org.ownerid = %s
                    WHERE moduleid = %s
            """),
            (user_id, module_id),
        )
        return result.fetch_one() is not None

    @staticmethod
    def get_info(conn: SwapDB, module_id: int) -> tuple[int, str, int] | None:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement(
                "SELECT moduleID, name, orgID FROM modules WHERE moduleID = %s"
            ),
            (module_id,),
        )

        tuple_result: tuple[int, str, int] | None = result.fetch_one()
        return tuple_result
