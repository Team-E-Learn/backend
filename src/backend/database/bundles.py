from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement


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

    bundle_id: int = bundle_result[0]

    for module_name in module_names:
        mod_result: SwapResult = cursor.execute(
            StringStatement("SELECT moduleID FROM modules WHERE name = %s"),
            (module_name,),
        )
        module_result: tuple[int] | None = mod_result.fetch_one()

        if module_result is None:
            continue

        module_id: int = module_result[0]

        _ = cursor.execute(
            StringStatement(
                "INSERT INTO bundle_modules (bundleID, moduleID) VALUES (%s, %s)"
            ),
            (bundle_id, module_id),
        )


class BundlesTable:

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
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

    # adds 2 bundles to the DB, each bundle contains a different set of modules
    # no alternative API call to add bundles, so this is the only way to add them
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
        for name, description, orgID in bundles:
            result = cursor.execute(
                StringStatement("SELECT 1 FROM bundles WHERE name = %s"), (name,)
            )

            if result.fetch_one() is not None:
                continue

            _ = cursor.execute(
                StringStatement(
                    "INSERT INTO bundles (name, description, orgID) VALUES (%s, %s, %s)"
                ),
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
