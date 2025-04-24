from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement

"""
Module for managing bundles in the database.
Provides operations for creating and populating the bundles table and linking modules to bundles.
"""


def add_modules_to_bundle(
    bundle_name: str, module_names: list[str], conn: SwapDB
) -> None:
    cursor: SwapCursor = conn.get_cursor()
    bund_result: SwapResult = cursor.execute(
        StringStatement("SELECT bundleID FROM bundles WHERE name = %s"), (bundle_name,)
    )

    bundle_result: tuple[int] | None = bund_result.fetch_one()

    if bundle_result is None:
        return None

    # Get the bundleID from the result
    bundle_id: int = bundle_result[0]

    # For each module in the list, get the moduleID and add it to the bundle_modules table
    for module_name in module_names:
        mod_result: SwapResult = cursor.execute(
            StringStatement("SELECT moduleID FROM modules WHERE name = %s"),
            (module_name,),
        )
        module_result: tuple[int] | None = mod_result.fetch_one()

        if module_result is None:
            continue

        module_id: int = module_result[0]

        cursor.execute(
            StringStatement(
                "INSERT INTO bundle_modules (bundleID, moduleID) VALUES (%s, %s)"
            ),
            (bundle_id, module_id),
        )

    return None


class BundlesTable:
    """Manages database operations for the bundles table.

    This class provides methods to create the bundles table and populate
    it with sample bundle data. Bundles are collections of modules that form
    a complete educational program or certification.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS bundles (
        bundleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );"""
            )
        )

    # Adds 2 bundles to the DB, each bundle contains a different set of modules
    # No alternative API call to add bundles, so this is the only way to add them
    @staticmethod
    def write_bundles(conn: SwapDB) -> None:
        # format is (name, description, orgID)
        bundles: list[tuple[str, str, int]] = [
            (
                "Computer Science BSc",
                "A bundle of modules for a Computer Science degree",
                1,
            ),
            (
                "Excel Certification",
                "A bundle of modules for an Excel certification",
                2,
            ),
        ]

        cursor: SwapCursor = conn.get_cursor()

        # Add each bundle to the bundles table
        for name, description, orgID in bundles:
            result = cursor.execute(
                StringStatement("SELECT 1 FROM bundles WHERE name = %s"), (name,)
            )

            if result.fetch_one() is not None:
                continue

            # Add the bundle to the bundles table
            cursor.execute(
                StringStatement(
                    "INSERT INTO bundles (name, description, orgID) VALUES (%s, %s, %s)"
                ),
                (name, description, orgID),
            )

        # List of modules to add to the CS bundle from modules.py
        add_modules_to_bundle(
            "Computer Science BSc",
            [
                "Team Software Engineering",
                "Networking Fundamentals",
                "Applied Programming Paradigms",
                "Personal Development",
            ],
            conn,
        )

        # List of modules to add to the Excel bundle from modules.py
        add_modules_to_bundle(
            "Excel Certification",
            [
                "Excel Certification",
                "Advanced Excel",
            ],
            conn,
        )
