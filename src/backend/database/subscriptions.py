from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


class SubscriptionsTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS subscriptions (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (userID, moduleID)
    );"""
        )

    # so you don't need to manually add subscriptions with http://127.0.0.1:5000/v1/org/1/module/1/user/1
    @staticmethod
    def write_subscriptions(conn: Connection[TupleRow]) -> None:
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

        cursor: Cursor[TupleRow] = conn.cursor()
        for user_id, module_id in subscriptions:
            _ = cursor.execute(
                "INSERT INTO subscriptions (userID, moduleID) VALUES (%s, %s)",
                (user_id, module_id),
            )

    @staticmethod
    def add_subscription(
        conn: Connection[TupleRow], user_id: int, module_id: int
    ) -> bool:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(
            "INSERT INTO subscriptions (userID, moduleID) VALUES (%s, %s)",
            (user_id, module_id),
        )
        conn.commit()
        return True
