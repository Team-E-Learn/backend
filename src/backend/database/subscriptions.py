from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement

"""
Module for managing user subscriptions to modules in the database.
Provides operations for creating, populating, and managing the many-to-many
relationship between users and the modules they are enrolled in or have access to.
"""


class SubscriptionsTable:
    """Manages database operations for the subscriptions table.

    This class provides methods to create the subscriptions table and manage
    user enrollment in modules. Each record represents a user's
    subscription to a specific module, forming a many-to-many relationship
    between users and modules they can access.
    """

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

    # So you don't need to manually add subscriptions with http://127.0.0.1:5000/v1/org/1/module/1/user/1
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

        # Write sample subscriptions to the database
        cursor: SwapCursor = conn.get_cursor()
        for user_id, module_id in subscriptions:
            _ = cursor.execute(
                StringStatement(
                    "INSERT INTO subscriptions (userID, moduleID) VALUES (%s, %s)"
                ),
                (user_id, module_id),
            )

    @staticmethod
    def add_subscription(conn: SwapDB, user_id: int, module_id: int) -> None:
        cursor: SwapCursor = conn.get_cursor()
        _ = cursor.execute(
            StringStatement(
                """
                INSERT INTO subscriptions (userID, moduleID) 
                VALUES (%s, %s)
                ON CONFLICT (userID, moduleID) DO NOTHING
                """
            ),
            (user_id, module_id),
        )
        conn.commit()

    @staticmethod
    def is_member(conn: SwapDB, user_id: int, module_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement(
                """
                SELECT 1
                FROM subscriptions
                WHERE userID = %s AND moduleID = %s
                """
            ),
            (user_id, module_id),
        )
        return result.fetch_one() is not None

    @staticmethod
    def can_read_lesson(conn: SwapDB, user_id: int, lesson_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("""SELECT 1 FROM lessons
                            JOIN subscriptions ON subscriptions.moduleID = lessons.moduleID
                            WHERE subscriptions.userID = %s AND lessons.lessonID = %s
                            """),
            (user_id, lesson_id),
        )
        return result.fetch_one() is not None
