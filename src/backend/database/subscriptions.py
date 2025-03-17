from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.statement import StringStatement


class SubscriptionsTable:

    @staticmethod
    def create(conn: SwapDB) -> None:
        _ = conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS subscriptions (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (userID, moduleID)
    );"""
            )
        )

    # so you don't need to manually add subscriptions with http://127.0.0.1:5000/v1/org/1/module/1/user/1
    @staticmethod
    def write_subscriptions(conn: SwapDB) -> None:
        # format is (userID, moduleID)
        subscriptions: list[tuple[int, int]] = [
            (3, 1),
            (3, 2),
            (3, 5),
            (3, 8),
            (4, 1),
            (4, 3),
            (4, 7),
            (4, 8),
        ]

        cursor: SwapCursor = conn.get_cursor()
        for user_id, module_id in subscriptions:
            _ = cursor.execute(
                StringStatement(
                    "INSERT INTO subscriptions (userID, moduleID) VALUES (%s, %s)"
                ),
                (user_id, module_id),
            )

    @staticmethod
    def add_subscription(conn: SwapDB, user_id: int, module_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        _ = cursor.execute(
            StringStatement(
                "INSERT INTO subscriptions (userID, moduleID) VALUES (%s, %s)"
            ),
            (user_id, module_id),
        )
        conn.commit()
        return True
