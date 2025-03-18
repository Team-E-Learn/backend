"""
Module for managing module-specific dashboard widgets in the database.
Provides operations for creating, populating, and retrieving dashboard widget data
that defines the personalized UI layout for each user within specific modules.
"""
from psycopg import Cursor
from psycopg.connection import Connection
from psycopg.rows import TupleRow


class ModuleDashboardTable:
    """Manages database operations for the module_dashboard table.

    This class provides methods to create the module_dashboard table and manage
    widget positions for user dashboards within specific modules. Each record
    represents a widget positioned on a user's personalized interface for a particular
    module.
    """

    @staticmethod
    def create(conn: Connection[TupleRow]) -> None:
        _ = conn.cursor().execute(
            """
    CREATE TABLE IF NOT EXISTS module_dashboard (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        widgetID VARCHAR(48) NOT NULL,
        widgetType VARCHAR(48) NOT NULL,
        x INT NOT NULL,
        y INT NOT NULL
    );"""
        )

    # for http://127.0.0.1:5000/v1/user/1234/dashboard/module/5678
    # no alternative API call to add module dashboard data, so this is the only way to add it
    @staticmethod
    def write_module_dashboard(conn: Connection[TupleRow]) -> None:
        # format is (userID, moduleID, widgetID, widgetType, x, y)
        module_dashboard: list[tuple[int, int, str, str, int, int]] = [
            (1, 1, "announcements_widget", "announcements", 10, 20),
            (1, 1, "info_widget", "info", 30, 20),
            (1, 1, "about_widget", "about", 10, 40),
            (1, 1, "grade_centre_widget", "grade_centre", 30, 40),
            (1, 1, "calendar_widget", "calendar", 10, 60),
            (2, 1, "announcements_widget", "announcements", 10, 20),
            (2, 1, "grade_centre_widget", "grade_centre", 30, 20),
            (2, 1, "calendar_widget", "calendar", 10, 40),
            (3, 1, "announcements_widget", "announcements", 10, 20),
            (3, 1, "info_widget", "info", 30, 20),
            (3, 1, "about_widget", "about", 10, 40),
            (3, 1, "grade_centre_widget", "grade_centre", 30, 40),
            (3, 1, "calendar_widget", "calendar", 10, 60),
            (4, 1, "announcements_widget", "announcements", 10, 20),
            (4, 1, "grade_centre_widget", "grade_centre", 30, 20),
            (4, 1, "calendar_widget", "calendar", 10, 40),
        ]

        # write sample module dashboard data to the database
        cursor: Cursor[TupleRow] = conn.cursor()
        for user_id, module_id, widget_id, widget_type, x, y in module_dashboard:
            _ = cursor.execute(
                "INSERT INTO module_dashboard (userID, moduleID, widgetID, widgetType, x, y)"
                + " VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, module_id, widget_id, widget_type, x, y),
            )

    @staticmethod
    def get_dashboard(
        conn: Connection[TupleRow], user_id: int, module_id: int
    ) -> list[tuple[int, int, str, str, int, int]]:
        cursor: Cursor[TupleRow] = conn.cursor()
        _ = cursor.execute(
            "SELECT * FROM module_dashboard WHERE userID = %s AND moduleID = %s",
            (user_id, module_id),
        )
        return cursor.fetchall()
