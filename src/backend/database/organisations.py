from psycopg.connection import Connection
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
        orgs = [
            ('University of Lincoln', 'A university in Lincoln', 4),
            ('Microsoft', 'A tech company', 2),
            ('Amazon', 'An online retailer', 2)
        ]

        cursor = conn.cursor()
        for name, description, ownerID in orgs:
            cursor.execute("SELECT 1 FROM organisations WHERE name = %s", (name,))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO organisations (name, description, ownerID) VALUES (%s, %s, %s)",
                    (name, description, ownerID))

    @staticmethod
    def org_exists(conn: Connection[TupleRow], org_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM organisations WHERE orgID = %s", (org_id,))
        return cursor.fetchone() is not None