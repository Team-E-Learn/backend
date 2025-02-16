from psycopg.connection import Connection
from psycopg.rows import TupleRow


class BundlesModulesTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS bundle_modules (
        bundleID INT REFERENCES bundles(bundleID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (bundleID, moduleID)
    );"""
        )
