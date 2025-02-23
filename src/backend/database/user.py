from psycopg.connection import Connection
from psycopg.rows import TupleRow


class UserTable:

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS users (
        userID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        accountType VARCHAR(16) NOT NULL,
        firstName VARCHAR(48) NOT NULL,
        lastName VARCHAR(48) NOT NULL,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );"""
        )

    @staticmethod
    def get_by_username(conn: Connection[TupleRow], username: str):
        cursor = conn.cursor()
        _ = cursor.execute(f"SELECT * FROM users WHERE username = %s;", (username,))
        return cursor.fetchone()

    @staticmethod
    def get_by_email(conn: Connection[TupleRow], email: str):
        cursor = conn.cursor()
        _ = cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        return cursor.fetchone()

    # this populates user_ids 1-4 with dummy data
    # no alternative API call to add users, so this is the only way to add them
    @staticmethod
    def write_users(conn: Connection[TupleRow]) -> None:
        users = [
            ('user', 'Alice', 'Smith', 'alice.smith', 'alice.smith@example.com'),
            ('admin', 'Bob', 'Johnson', 'bob.johnson', 'bob.johnson@example.com'),
            ('user', 'Carol', 'Williams', 'carol.williams', 'carol.williams@example.com'),
            ('admin', 'David', 'Brown', 'david.brown', 'david.brown@example.com')
        ]

        cursor = conn.cursor()
        for accountType, firstName, lastName, username, email in users:
            cursor.execute("SELECT 1 FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO users (accountType, firstName, lastName, username, email) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (accountType, firstName, lastName, username, email))

    # this function is called from src/routes/user/profile.py
    @staticmethod
    def get_user_profile(conn: Connection[TupleRow], user_id: int) -> dict[str, str]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, email, firstName, lastName, accountType FROM users WHERE userID = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        if user:
            return {
                "username": user[0],
                "email": user[1],
                "firstName": user[2],
                "lastName": user[3],
                "accountType": user[4]
            }
        else:
            return {"error": "User not found"}

    # this function is called from src/routes/user/user.py
    @staticmethod
    def user_exists(conn: Connection[TupleRow], user_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE userID = %s", (user_id,))
        return cursor.fetchone() is not None

