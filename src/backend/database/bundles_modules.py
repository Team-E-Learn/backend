"""
Module for managing the relationships between bundles and modules.
Provides the operation for creating the bundle_modules junction table that establishes
many-to-many relationships between bundles and their constituent modules.
"""
from psycopg.connection import Connection
from psycopg.rows import TupleRow


class BundlesModulesTable:
    """Manages the database operation for the bundle_modules junction table.

    This class provides a method to create the bundle_modules table that establishes
    the many-to-many relationship between bundles and modules. Each record in this
    table represents a module's inclusion in a specific bundle.
    """

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
