from psycopg.connection import Connection
from psycopg.rows import TupleRow


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

        cursor.execute("SELECT bundleID FROM bundles WHERE name = %s", ('Computer Science BSc',))
        bundle_id = cursor.fetchone()[0]
        module_names = [
            'Team Software Engineering',
            'Networking Fundamentals',
            'Applied Programming Paradigms',
            'Personal Development'
        ]
        for module_name in module_names:
            cursor.execute("SELECT moduleID FROM modules WHERE name = %s", (module_name,))
            module_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO bundle_modules (bundleID, moduleID) VALUES (%s, %s)",
                (bundle_id, module_id)
            )
