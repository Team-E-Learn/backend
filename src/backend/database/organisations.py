from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


class OrganisationsTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS organisations (
        orgID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) UNIQUE NOT NULL,
        description VARCHAR(100) NOT NULL,
        ownerID INT REFERENCES users(userID) NOT NULL
    );"""
        )

    # adds 3 orgs to the DB, user_id 3 is the owner of the first org, user_id 2 is the owner of the other two
    # no alternative API call to add organisations, so this is the only way to add them
    @staticmethod
    def write_orgs(conn: Connection[TupleRow]) -> None:
        # format is (name, description, ownerID (userID who owns the org))
        orgs: list[tuple[str, str, int]] = [
            ("University of Lincoln", "A university in Lincoln", 4),
            ("Microsoft", "A tech company", 2),
            ("Amazon", "An online retailer", 2),
        ]

        cursor: Cursor[TupleRow] = conn.cursor()
        for name, description, ownerID in orgs:
            _ = cursor.execute("SELECT 1 FROM organisations WHERE name = %s", (name,))

            if cursor.fetchone() is not None:
                continue

            _ = cursor.execute(
                "INSERT INTO organisations (name, description, ownerID) VALUES (%s, %s, %s)",
                (name, description, ownerID),
            )

    @staticmethod
    def org_exists(conn: Connection[TupleRow], org_id: int) -> bool:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute("SELECT 1 FROM organisations WHERE orgID = %s", (org_id,))
        return cursor.fetchone() is not None
