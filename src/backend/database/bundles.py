from psycopg.connection import Connection
from psycopg.rows import TupleRow


def add_modules_to_bundle(bundle_name, module_names, conn: Connection[TupleRow]) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT bundleID FROM bundles WHERE name = %s", (bundle_name,))
    bundle_id = cursor.fetchone()[0]
    for module_name in module_names:
        cursor.execute("SELECT moduleID FROM modules WHERE name = %s", (module_name,))
        module_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO bundle_modules (bundleID, moduleID) VALUES (%s, %s)",
            (bundle_id, module_id)
        )


class BundlesTable:

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
        bundles = [
            ('Computer Science BSc', 'A bundle of modules for a Computer Science degree', 1),
            ('Excel Certification', 'A bundle of modules for an Excel certification', 2)
        ]

        cursor = conn.cursor()
        for name, description, orgID in bundles:
            cursor.execute("SELECT 1 FROM bundles WHERE name = %s", (name,))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO bundles (name, description, orgID) VALUES (%s, %s, %s)",
                    (name, description, orgID))

        # list of modules to add to the CS bundle from modules.py
        add_modules_to_bundle('Computer Science BSc', [
            'Team Software Engineering',
            'Networking Fundamentals',
            'Applied Programming Paradigms',
            'Personal Development'
        ], conn)

        # list of modules to add to the Excel bundle from modules.py
        add_modules_to_bundle('Excel Certification', [
            'Excel Certification',
            'Advanced Excel',
        ], conn)
