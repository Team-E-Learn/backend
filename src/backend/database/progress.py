"""
Module for tracking and managing user progress through modules in the database.
Provides the operation for creating progress records that store
detailed information about a user's advancement through specific modules.
"""
from psycopg.connection import Connection
from psycopg.rows import TupleRow


class ProgressTable:
    """Manages database operations for the progress table.

    This class provides a method to create the progress table which stores
    user progress data for educational modules. Each record represents a user's
    progress through a specific module, with detailed information stored in a
    JSON structure that can accommodate various progress tracking schemas.
    """

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS progress (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        progress JSON NOT NULL,
        primary key (userID, moduleID)
    );"""
        )
