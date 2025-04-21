from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
"""
Module for managing organisations in the database.
Provides operations for creating, populating, and validating organisations
that can own modules and are managed by user accounts.
"""


class OrganisationsTable:
    """Manages database operations for the organisations table.

    This class provides methods to create the organisations table and manage
    organisation data. Each organisation has a unique name, description, and
    an owner who is referenced by their user ID. organisations serve as containers
    for modules and other content.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        cursor: SwapCursor = conn.get_cursor()
        cursor.execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS organisations (
        orgID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) UNIQUE NOT NULL,
        description VARCHAR(100) NOT NULL,
        ownerID INT REFERENCES users(userID) NOT NULL
    );"""
            )
        )

    @staticmethod
    def write_org(conn: SwapDB, name: str, description: str, owner_id: int) -> int | None:
        cursor: SwapCursor = conn.get_cursor()

        # Check if the organization already exists
        result: SwapResult = cursor.execute(
            StringStatement("SELECT orgID FROM organisations WHERE name = %s"), (name,)
        )
        orgID = result.fetch_one()

        # If it does, delete its modules
        if orgID is not None:
            cursor.execute(
                StringStatement("DELETE FROM modules WHERE orgID = %s"),
                (orgID[0],)
            )
            conn.commit()
            # Return the orgID of the organisation
            return orgID[0]

        # Insert the organization
        result = cursor.execute(
            StringStatement(
                "INSERT INTO organisations (name, description, ownerID) VALUES (%s, %s, %s) RETURNING orgID"
            ),
            (name, description, owner_id),
        )
        # Return the orgID of the organisation
        return result.fetch_one()[0]

    # Adds 3 orgs to the DB, user_id 3 is the owner of the first org, user_id 2 is the owner of the other two
    # No alternative API call to add organisations, so this is the only way to add them
    @staticmethod
    def write_orgs(conn: SwapDB) -> None:
        # Format is (name, description, ownerID (userID who owns the org))
        orgs: list[tuple[str, str, int]] = [
            ("University of Lincoln", "A university in Lincoln", 4),
            ("Microsoft", "A tech company", 2),
            ("Amazon", "An online retailer", 2),
        ]

        # Write sample organisations to the database
        cursor: SwapCursor = conn.get_cursor()
        for name, description, ownerID in orgs:
            result: SwapResult = cursor.execute(
                StringStatement("SELECT 1 FROM organisations WHERE name = %s"), (name,)
            )

            if result.fetch_one() is not None:
                # Skip if the organisation already exists
                continue

            # Insert organisation into organisations table
            cursor.execute(
                StringStatement(
                    "INSERT INTO organisations (name, description, ownerID) VALUES (%s, %s, %s)"
                ),
                (name, description, ownerID),
            )

    @staticmethod
    def org_exists(conn: SwapDB, org_id: int) -> bool:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT 1 FROM organisations WHERE orgID = %s"), (org_id,)
        )
        return result.fetch_one() is not None
