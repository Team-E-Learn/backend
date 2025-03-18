"""
Module for managing user subscriptions to modules in the database.
Provides operations for creating, populating, and managing the many-to-many
relationship between users and the modules they are enrolled in or have access to.
"""
from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


class SubscriptionsTable:
    """Manages database operations for the subscriptions table.

    This class provides methods to create the subscriptions table and manage
    user enrollment in modules. Each record represents a user's
    subscription to a specific module, forming a many-to-many relationship
    between users and modules they can access.
    """

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

    # So you don't need to manually add subscriptions with http://127.0.0.1:5000/v1/org/1/module/1/user/1
    @staticmethod
    def write_subscriptions(conn: Connection[TupleRow]) -> None:
        # Format is (userID, moduleID)
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

        # Write sample subscriptions to the database
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
