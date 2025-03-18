"""
Module for managing relationships between teachers and modules in the database.
Provides operations for establishing and maintaining the many-to-many relationship
between users (in teacher roles) and the modules they teach.
"""
from psycopg.connection import Connection
from psycopg.rows import TupleRow


class ModuleTeachersTable:
    """Manages the database operation for the module_teachers junction table.

    This class provides a method to create the relationships between
    teachers and modules. Each record represents a teacher assigned to teach
    a particular module, forming a many-to-many relationship
    between users and modules.
    """

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS module_teachers (
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        userID INT REFERENCES users(userID) NOT NULL,
        PRIMARY KEY (moduleID, userID)
    );"""
        )
