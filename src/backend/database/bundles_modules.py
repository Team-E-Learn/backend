from lib.dataswap.database import SwapDB
from lib.dataswap.statement import StringStatement
"""
Module for managing the relationships between bundles and modules.
Provides the operation for creating the bundle_modules junction table that establishes
many-to-many relationships between bundles and their constituent modules.
"""


class BundlesModulesTable:
    """Manages the database operation for the bundle_modules junction table.

    This class provides a method to create the bundle_modules table that establishes
    the many-to-many relationship between bundles and modules. Each record in this
    table represents a module's inclusion in a specific bundle.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS bundle_modules (
        bundleID INT REFERENCES bundles(bundleID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (bundleID, moduleID)
    );"""
            )
        )
