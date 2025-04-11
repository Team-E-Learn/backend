from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
"""
Module for managing user dashboard widgets in the database.
Provides operations for creating, populating, and retrieving dashboard widget data
that defines the personalized UI layout for each user.
"""


class DashboardTable:
    """Manages database operations for the dashboard table.

    This class provides methods to create the dashboard table and manage
    widget positions for user dashboards. Each record represents a widget
    positioned on a user's personalized dashboard interface.
    """

    @staticmethod
    def create(conn: SwapDB) -> None:
        conn.get_cursor().execute(
            StringStatement(
                """
    CREATE TABLE IF NOT EXISTS dashboard (
        widgetID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        userID INT REFERENCES users(userID) NOT NULL,
        widgetType VARCHAR(48) NOT NULL,
        x INT NOT NULL,
        y INT NOT NULL
    );"""
            )
        )

    # For http://127.0.0.1:5000/v1/user/1/dashboard
    # No alternative API call to add dashboard data, so this is the only way to add it
    @staticmethod
    def write_dashboard(conn: SwapDB) -> None:
        # Format is (user_id, widget_type, x, y)
        dashboard: list[tuple[int, str, int, int]] = [
            (1, "announcements", 10, 20),
            (1, "info", 30, 20),
            (1, "about", 10, 40),
            (1, "grade_centre", 30, 40),
            (1, "calendar", 10, 60),
            (2, "announcements", 10, 20),
            (2, "grade_centre", 30, 20),
            (2, "calendar", 10, 40),
            (3, "announcements", 10, 20),
            (3, "info", 30, 20),
            (3, "about", 10, 40),
            (3, "grade_centre", 30, 40),
            (3, "calendar", 10, 60),
            (4, "announcements", 10, 20),
            (4, "grade_centre", 30, 20),
            (4, "calendar", 10, 40),
        ]

        # Write sample dashboard data to the dashboard table
        cursor: SwapCursor = conn.get_cursor()
        for user_id, widget_type, x, y in dashboard:
            cursor.execute(
                StringStatement(
                    "INSERT INTO dashboard (userID, widgetType, x, y) VALUES (%s, %s, %s, %s)"
                ),
                (user_id, widget_type, x, y),
            )

    @staticmethod
    def get_dashboard(
        conn: SwapDB, user_id: int
    ) -> list[tuple[int, str, str, int, int]]:
        cursor: SwapCursor = conn.get_cursor()
        result: SwapResult = cursor.execute(
            StringStatement("SELECT * FROM dashboard WHERE userID = %s"), (user_id,)
        )
        tup_res: list[tuple[int, str, str, int, int]] | None = result.fetch_all()
        return [] if tup_res is None else tup_res
