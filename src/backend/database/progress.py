from lib.dataswap.database import SwapDB
from lib.dataswap.statement import StringStatement


class ProgressTable:

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS progress (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        progress JSON NOT NULL,
        primary key (userID, moduleID)
    );"""
            )
        )
