from lib.dataswap.database import SwapDB
from lib.dataswap.statement import StringStatement


class ModuleTeachersTable:

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS module_teachers (
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        userID INT REFERENCES users(userID) NOT NULL,
        PRIMARY KEY (moduleID, userID)
    );"""
            )
        )
