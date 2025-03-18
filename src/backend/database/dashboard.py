"""
Module for managing user dashboard widgets in the database.
Provides operations for creating, populating, and retrieving dashboard widget data
that defines the personalized UI layout for each user.
"""
from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import TupleRow


class DashboardTable:
    """Manages database operations for the dashboard table.

    This class provides methods to create the dashboard table and manage
    widget positions for user dashboards. Each record represents a widget
    positioned on a user's personalized dashboard interface.
    """

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS dashboard (
        widgetID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        userID INT REFERENCES users(userID) NOT NULL,
        widgetType VARCHAR(48) NOT NULL,
        x INT NOT NULL,
        y INT NOT NULL
    );"""
        )

    # for http://127.0.0.1:5000/v1/user/1/dashboard
    # no alternative API call to add dashboard data, so this is the only way to add it
    @staticmethod
    def write_dashboard(conn: Connection[TupleRow]) -> None:
        # format is (user_id, widget_type, x, y)
        dashboard: list[tuple[int, str, int, int]] = [
            (1, 'announcements', 10, 20),
            (1, 'info', 30, 20),
            (1, 'about', 10, 40),
            (1, 'grade_centre', 30, 40),
            (1, 'calendar', 10, 60),
            (2, 'announcements', 10, 20),
            (2, 'grade_centre', 30, 20),
            (2, 'calendar', 10, 40),
            (3, 'announcements', 10, 20),
            (3, 'info', 30, 20),
            (3, 'about', 10, 40),
            (3, 'grade_centre', 30, 40),
            (3, 'calendar', 10, 60),
            (4, 'announcements', 10, 20),
            (4, 'grade_centre', 30, 20),
            (4, 'calendar', 10, 40)
        ]

        # write sample dashboard data to the dashboard table
        cursor: Cursor[TupleRow] = conn.cursor()
        for user_id, widget_type, x, y in dashboard:
            _ = cursor.execute(
                "INSERT INTO dashboard ( userID, widgetType, x, y) VALUES (%s, %s, %s, %s)",
                (user_id, widget_type, x, y)
            )


    @staticmethod
    def get_dashboard(conn: Connection[TupleRow], user_id: int) -> list[tuple[int, str, str, int, int]]:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute("SELECT * FROM dashboard WHERE userID = %s", (user_id,))
        return cursor.fetchall()
