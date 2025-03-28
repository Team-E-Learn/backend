from lib.dataswap.database import SwapDB
from lib.dataswap.statement import StringStatement
"""
Module for managing relationships between teachers and modules in the database.
Provides operations for establishing and maintaining the many-to-many relationship
between users (in teacher roles) and the modules they teach.
"""


class ModuleTeachersTable:
    """Manages the database operation for the module_teachers junction table.

    This class provides a method to create the relationships between
    teachers and modules. Each record represents a teacher assigned to teach
    a particular module, forming a many-to-many relationship
    between users and modules.
    """

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
