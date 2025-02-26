from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


class ModulesTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS modules (
        moduleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );"""
        )

    # adds 8 modules to the DB, 4 are owned by org_id 1, 2 are owned by org_id 2, 2 are owned by org_id 3
    # no alternative API call to add modules, so this is the only way to add them
    @staticmethod
    def write_modules(conn: Connection[TupleRow]) -> None:
        # format is (name, description, orgID)
        modules: list[tuple[str, str, int]] = [
            ("Personal Development", "Learn how to develop yourself", 1),
            ("Team Software Engineering", "Team-based software engineering project", 1),
            ("Networking Fundamentals", "Basics of networking", 1),
            ("Applied Programming Paradigms", "Different programming paradigms", 1),
            ("Excel Certification", "Get certified in Excel", 2),
            ("Advanced Excel", "Advanced techniques in Excel", 2),
            ("Data Analysis", "Learn data analysis techniques", 3),
            ("Machine Learning", "Introduction to machine learning", 3),
        ]

        cursor: Cursor[TupleRow] = conn.cursor()
        for name, description, orgID in modules:
            _ = cursor.execute("SELECT 1 FROM modules WHERE name = %s", (name,))

            if cursor.fetchone() is not None:
                continue

            _ = cursor.execute(
                "INSERT INTO modules (name, description, orgID) VALUES (%s, %s, %s)",
                (name, description, orgID),
            )

    @staticmethod
    def module_exists(conn: Connection[TupleRow], module_id: int) -> bool:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute("SELECT 1 FROM modules WHERE moduleID = %s", (module_id,))
        return cursor.fetchone() is not None

    @staticmethod
    def module_owned_by_org(
        conn: Connection[TupleRow], module_id: int, org_id: int
    ) -> bool:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(
            "SELECT 1 FROM modules WHERE moduleID = %s AND orgID = %s",
            (module_id, org_id),
        )
        return cursor.fetchone() is not None
