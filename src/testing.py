from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
from typing import Any

# todo a progress test will need to be build in the future

# This testing system is designed to work with the provided sample data
# therefore for tests to succeed "populate_dummy_data(conn)" in main.py must be run first

# Tests to check sample data is stored and retrieved correctly from the database

def user_test(conn: SwapDB) -> None:
    # Expected users in the database
    expected_users: list[tuple[str, str, str, str, str, str]] = [
        (
            "user",
            "Alice",
            "Smith",
            "alice.smith",
            "alice.smith@example.com",
            "WVTBSKRNKORNCBMI",
        ),
        (
            "admin",
            "Bob",
            "Johnson",
            "bob.johnson",
            "bob.johnson@example.com",
            "KEQWOVVUJDIFQSJD",
        ),
        (
            "user",
            "Carol",
            "Williams",
            "carol.williams",
            "carol.williams@example.com",
            "HARAUJMIXYGDSRLA",
        ),
        (
            "admin",
            "David",
            "Brown",
            "david.brown",
            "david.brown@example.com",
            "OSQBCMPVGVZTUGPO",
        ),
    ]

    # Read users from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT accountType, firstName, lastName, username, email, totpSecret FROM users")
    )
    users: list[tuple[str, str, str, str, str, str]] | None = result.fetch_all()

    # Compare expected and retrieved users
    assert users == expected_users, f"Expected: {expected_users}, Got: {users}"
    print("\n>> User data write and read test passed!")

def organisations_test(conn: SwapDB) -> None:
    # Expected organisations
    expected_orgs: list[tuple[str, str, int]] = [
        ("University of Lincoln", "A university in Lincoln", 4),
        ("Microsoft", "A tech company", 2),
        ("Amazon", "An online retailer", 2),
    ]

    # read organisations from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT name, description, ownerID FROM organisations")
    )
    orgs: list[tuple[str, str, int]] | None = result.fetch_all()

    # compare expected and retrieved organisations
    assert orgs == expected_orgs, f"Original organisations: {expected_orgs},\n Retrieved organisations: {orgs}"
    print(">> Organisation write and read test passed!")


def modules_test(conn: SwapDB) -> None:
    # Expected modules
    expected_modules: list[tuple[str, str, int]] = [
        ("Personal Development", "Learn how to develop yourself", 1),
        ("Team Software Engineering", "Team-based software engineering project", 1),
        ("Networking Fundamentals", "Basics of networking", 1),
        ("Applied Programming Paradigms", "Different programming paradigms", 1),
        ("Excel Certification", "Get certified in Excel", 2),
        ("Advanced Excel", "Advanced techniques in Excel", 2),
        ("Data Analysis", "Learn data analysis techniques", 3),
        ("Machine Learning", "Introduction to machine learning", 3),
    ]

    # Read modules from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT name, description, orgID FROM modules")
    )
    modules: list[tuple[str, str, int]] | None = result.fetch_all()

    # Compare expected and retrieved modules
    assert modules == expected_modules, f"Original modules: {expected_modules},\n Retrieved modules: {modules}"
    print(">> Module write and read test passed!")


def lessons_test(conn: SwapDB) -> None:
    # Expected lessons
    expected_lessons: list[tuple[int, str, dict[str, Any]]] = [
        (1, "Introduction", {"content": "Welcome to the introduction"}),
        (1, "Lesson 1", {"content": "This is lesson 1"}),
        (1, "Lesson 2", {"content": "This is lesson 2"}),
        (1, "Lesson 3", {"content": "This is lesson 3"}),
        (2, "Introduction", {"content": "Welcome to the introduction"}),
        (2, "Lesson 1", {"content": "This is lesson 1"}),
        (2, "Lesson 2", {"content": "This is lesson 2"}),
        (2, "Lesson 3", {"content": "This is lesson 3"}),
        (3, "Introduction", {"content": "Welcome to the introduction"}),
        (3, "Lesson 1", {"content": "This is lesson 1"}),
        (3, "Lesson 2", {"content": "This is lesson 2"}),
        (3, "Lesson 3", {"content": "This is lesson 3"}),
        (4, "Introduction", {"content": "Welcome to the introduction"}),
        (4, "Lesson 1", {"content": "This is lesson 1"}),
        (4, "Lesson 2", {"content": "This is lesson 2"}),
        (4, "Lesson 3", {"content": "This is lesson 3"}),
    ]

    # Read lessons from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT moduleID, title, sections FROM lessons")
    )
    lessons: list[tuple[int, str, dict[str, Any]]] | None = result.fetch_all()

    # Compare expected and retrieved lessons
    assert lessons == expected_lessons, f"Original lessons: {expected_lessons},\n Retrieved lessons: {lessons}"
    print(">> Lesson write and read test passed!")


def bundle_test(conn: SwapDB) -> None:
    # Expected bundles
    expected_bundles: list[tuple[str, str]] = [
        ('Computer Science BSc', 'A bundle of modules for a Computer Science degree'),
        ('Excel Certification', 'A bundle of modules for an Excel certification')
    ]

    # Read bundles from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT name, description FROM bundles")
    )
    bundles: list[tuple[str, str]] | None = result.fetch_all()

    # Compare expected and retrieved bundles
    assert bundles == expected_bundles, f"Original bundles: {expected_bundles},\n Retrieved bundles: {bundles}"
    print(">> Bundle write and read test passed!")


def bundle_modules_test(conn: SwapDB) -> None:
    # Expected modules in bundles
    expected_modules: list[tuple[str,]] = [
        ("Applied Programming Paradigms",),
        ("Networking Fundamentals",),
        ("Personal Development",),
        ("Team Software Engineering",)
    ]

    # Get modules in Computer Science BSc bundle
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("""
            SELECT m.name FROM modules m
            JOIN bundle_modules bm ON m.moduleID = bm.moduleID
            JOIN bundles b ON bm.bundleID = b.bundleID
            WHERE b.name = 'Computer Science BSc'
            ORDER BY m.name
        """)
    )
    modules: list[tuple[str,]] | None = result.fetch_all()

    # Compare expected and retrieved modules
    assert modules == expected_modules, f"Expected: {expected_modules}, Got: {modules}"
    print(">> Bundle modules relationship write and read test passed!")


def block_test(conn: SwapDB) -> None:
    # Expected blocks
    expected_blocks: list[tuple[int, int, int, dict[str, str]]] = [
        (1,1,1,
            {
                "question_content": "what is the colour of the sky?",
                "question_answer": "blue",
            },
        ),
        (1, 2, 2, {"text": "The sky is blue"}),
        (1, 3, 3, {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
        (1, 4, 4, {"image_url": "https://www.example.com/image.jpg"})
    ]

    # Read blocks from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(StringStatement(
            "SELECT blockType, blockOrder, data FROM blocks WHERE lessonID = 1"
        )
    )
    block_results: list[tuple[int, int, dict[str, str]]] | None = result.fetch_all()

    # Recreate blocks list for comparison
    blocks: list[tuple[int, int, int, dict[str, str]]] = []
    for block_type, order, data_dict in block_results:
        blocks.append((1, block_type, order, data_dict))

    # Compare expected and retrieved blocks
    assert blocks == expected_blocks, f"Original blocks: {expected_blocks},\n Retrieved blocks: {blocks}"
    print(">> Block write and read test passed!")


def subscriptions_table_test(conn: SwapDB) -> None:
    # Expected subscription data
    expected_subs: list[tuple[int, int]] = [(3, 1), (3, 2), (3, 5), (3, 8)]

    # Query database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT userID, moduleID FROM subscriptions WHERE userID = 3")
    )
    subs: list[tuple[int, int]] | None = result.fetch_all()

    # Compare expected and retrieved subscriptions
    assert subs == expected_subs, f"Expected: {expected_subs}, Got: {subs}"
    print(">> Subscriptions write and read test passed!")


def module_dashboard_test(conn: SwapDB) -> None:
    # Expected dashboard settings
    expected_module_dashboard: list[tuple[int, int, str, str, int, int]] = [
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

    # Read dashboard settings from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT userID, moduleID, widgetID, widgetType, x, y FROM module_dashboard")
    )
    dashboard: list[tuple[int, int, str, str, int, int]] | None = result.fetch_all()

    # Recreate module dashboard settings list for comparison
    assert dashboard == expected_module_dashboard, f"Expected: {expected_module_dashboard}, Got: {dashboard}"
    print(">> Dashboard settings write and read test passed!")


def module_codes_test(conn: SwapDB) -> None:
    # Expected module codes
    expected_codes: list[tuple[int, str, list[int]]] = [
        (1, 'INTRO1', [1, 2, 3]),
        (2, 'ADVMOD', [4, 5, 6]),
        (3, 'ALLMOD', [1, 2, 3, 4, 5, 6, 7, 8])
    ]

    # Read module codes from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT code_id, code, module_ids FROM module_codes")
    )
    codes: list[tuple[int, str, list[int]]] | None = result.fetch_all()

    # Recreate module codes list for comparison
    assert codes == expected_codes, f"Expected: {expected_codes}, Got: {codes}"
    print(">> Module codes write and read test passed!")


def dashboard_test(conn: SwapDB) -> None:
    # Expected module dashboard data
    expected_dashboard: list[tuple[int, str, int, int]] = [
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

    # Read dashboards from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT userID, widgetType, x, y FROM dashboard")
    )
    dashboard: list[tuple[int, str, int, int]] | None = result.fetch_all()

    # Compare expected and retrieved dashboards
    assert dashboard == expected_dashboard, f"Expected: {expected_dashboard}, Got: {dashboard}"
    print(">> Module dashboard write and read test passed!")


# todo then I'm also going to check the same read-out data can then be read from the API as correct as well.


def run_tests(conn: SwapDB) -> None:
    try:
        user_test(conn)
        organisations_test(conn)
        modules_test(conn)
        lessons_test(conn)
        bundle_test(conn)
        bundle_modules_test(conn)
        block_test(conn)
        subscriptions_table_test(conn)
        module_dashboard_test(conn)
        module_codes_test(conn)
        dashboard_test(conn)
        print("All tests passed!\n")
    except AssertionError as e:
        input(f"Test failed: {e}")
