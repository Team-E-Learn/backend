from lib.dataswap.database import SwapDB
from lib.dataswap.statement import StringStatement


class BundlesModulesTable:

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
