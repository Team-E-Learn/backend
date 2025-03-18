"""
Module for managing bundles in the database.
Provides operations for creating and populating the bundles table and linking modules to bundles.
"""
from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


def add_modules_to_bundle(
    bundle_name: str, module_names: list[str], conn: Connection[TupleRow]
) -> None:
    """Associate multiple modules with a bundle by name.

        Args:
            bundle_name: Name of the bundle to add modules to
            module_names: List of module names to associate with the bundle
            conn: Database connection object
        """
    cursor = conn.cursor()
    _ = cursor.execute("SELECT bundleID FROM bundles WHERE name = %s", (bundle_name,))
    bundle_result: TupleRow | None = cursor.fetchone()
    if bundle_result is None:
        return

    # get the bundleID from the result
    bundle_id: int = bundle_result[0]

    # for each module in the list, get the moduleID and add it to the bundle_modules table
    for module_name in module_names:
        _ = cursor.execute(
            "SELECT moduleID FROM modules WHERE name = %s", (module_name,)
        )
        module_result: TupleRow | None = cursor.fetchone()
        if module_result is None:
            continue

        module_id: int = module_result[0]

        _ = cursor.execute(
            "INSERT INTO bundle_modules (bundleID, moduleID) VALUES (%s, %s)",
            (bundle_id, module_id),
        )


class BundlesTable:
    """Manages database operations for the bundles table.

    This class provides methods to create the bundles table and populate
    it with sample bundle data. Bundles are collections of modules that form
    a complete educational program or certification.
    """

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS bundles (
        bundleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );"""
        )

    # adds 2 bundles to the DB, each bundle contains a different set of modules
    # no alternative API call to add bundles, so this is the only way to add them
    @staticmethod
    def write_bundles(conn: Connection[TupleRow]) -> None:
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

        # add each bundle to the bundles table
        cursor: Cursor[TupleRow] = conn.cursor()
        for name, description, orgID in bundles:
            _ = cursor.execute("SELECT 1 FROM bundles WHERE name = %s", (name,))
            if cursor.fetchone() is not None:
                continue

            _ = cursor.execute(
                "INSERT INTO bundles (name, description, orgID) VALUES (%s, %s, %s)",
                (name, description, orgID),
            )

        # list of modules to add to the CS bundle from modules.py
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

        # list of modules to add to the Excel bundle from modules.py
        add_modules_to_bundle(
            "Excel Certification",
            [
                "Excel Certification",
                "Advanced Excel",
            ],
            conn,
        )
