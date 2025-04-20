from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
from typing import Any

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
            "teacher",
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
            "teacher",
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
    expected_lessons: list[tuple[int, str]] = [
            (1, "Introduction"),
            (1, "Lesson 1"),
            (1, "Lesson 2"),
            (1, "Lesson 3"),
            (2, "Introduction"),
            (2, "Lesson 1",),
            (2, "Lesson 2"),
            (2, "Lesson 3"),
            (3, "Introduction"),
            (3, "Lesson 1"),
            (3, "Lesson 2"),
            (3, "Lesson 3"),
            (4, "Introduction"),
            (4, "Lesson 1"),
            (4, "Lesson 2"),
            (4, "Lesson 3"),
        ]

    # Read lessons from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(
        StringStatement("SELECT moduleID, title FROM lessons")
    )
    lessons: list[tuple[int, str]] | None = result.fetch_all()

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
    expected_blocks: list[tuple[int, int, int, str, dict[str, str]]] = [
        (1, 1, 1, "Sky Question",
            {
                "question_content": "what is the colour of the sky?",
                "question_answer": "blue",
            },
        ),
        (1, 2, 2, "Sky Text", {"text": "The sky is blue"}),
        (1, 3, 3, "Sky Video", {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
        (1, 4, 4, "Sky Image", {"image_url": "https://www.example.com/image.jpg"})
    ]

    # Read blocks from the database
    cursor: SwapCursor = conn.get_cursor()
    result: SwapResult = cursor.execute(StringStatement(
            "SELECT blockType, blockOrder, blockName, data FROM blocks WHERE lessonID = 1"
        )
    )
    block_results: list[tuple[int, int, str, dict[str, str]]] | None = result.fetch_all()

    # Recreate blocks list for comparison
    blocks: list[tuple[int, int, int, str, dict[str, str]]] = []
    for block_type, order, block_name, data_dict in block_results:
        blocks.append((1, block_type, order, block_name, data_dict))

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


# API endpoint tests to check if the API is working correctly

def test_endpoint(endpoint: str, expected_data: Any,
              method: str = "GET",
              data: dict[str, Any] | None = None,
              headers: dict[str, str] | None = None) -> None:
    from main import front  # Imported here to avoid circular import issues

    # Use Flask's test client
    test_client = front.get_test_client()

    # Call the API endpoint
    if method.upper() == "GET":
        response = test_client.get(endpoint, headers=headers)
    elif method.upper() == "POST":
        response = test_client.post(endpoint, data=data, headers=headers)
    elif method.upper() == "PUT":
        response = test_client.put(endpoint, data=data, headers=headers)
    elif method.upper() == "DELETE":
        response = test_client.delete(endpoint, data=data, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    # Check the response is as expected
    response_data: Any = response.get_json()
    assert response_data == expected_data, f"Expected: {expected_data}, Got: {response_data}"
    print(f">> API endpoint test passed for {method.upper()} {endpoint}!")

def subscriptions_endpoint_test() -> None:
    # Expected response
    expected_response: list[dict[str, Any]] = [
        {
            "org_name": "University of Lincoln",
            "org_id": 1,
            "bundles": [
                {
                    "bundle_id": 1,
                    "bundle_name": "Computer Science BSc",
                    "modules": [
                        {
                            "name": "Networking Fundamentals",
                            "module_id": 3
                        },
                        {
                            "name": "Personal Development",
                            "module_id": 1
                        }
                    ]
                }
            ],
            "modules": []
        },
        {
            "org_name": "Amazon",
            "org_id": 3,
            "bundles": [],
            "modules": [
                {
                    "name": "Machine Learning",
                    "module_id": 8
                },
                {
                    "name": "Data Analysis",
                    "module_id": 7
                }
            ]
        }
    ]

    # Call the API endpoint
    test_endpoint("/v1/user/4/subscriptions", expected_response)


def profile_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, str] = {
        "username": "alice.smith",
        "email": "alice.smith@example.com",
        "firstName": "Alice",
        "lastName": "Smith",
        "accountType": "user"
    }

    # Call the API endpoint
    test_endpoint("/v1/user/1/profile", expected_response)


def module_dashboard_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, Any] = {
        "elements": [
            {
                "id": "announcements_widget",
                "type": "announcements",
                "position": {
                    "x": 10,
                    "y": 20
                }
            },
            {
                "id": "grade_centre_widget",
                "type": "grade_centre",
                "position": {
                    "x": 30,
                    "y": 20
                }
            },
            {
                "id": "calendar_widget",
                "type": "calendar",
                "position": {
                    "x": 10,
                    "y": 40
                }
            }
        ]
    }

    # Call the API endpoint
    test_endpoint("/v1/user/2/dashboard/module/1", expected_response)


def dashboard_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, Any] = {
        "elements": [
            {
                "id": 2,
                "type": "announcements",
                "position": {
                    "x": 10,
                    "y": 20
                }
            },
            {
                "id": 2,
                "type": "grade_centre",
                "position": {
                    "x": 30,
                    "y": 20
                }
            },
            {
                "id": 2,
                "type": "calendar",
                "position": {
                    "x": 10,
                    "y": 40
                }
            }
        ]
    }

    # Call the API endpoint
    test_endpoint("/v1/user/2/dashboard", expected_response)


def create_organisation_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "name": "Example Organisation",
        "description": "An example Organisation description",
        "modules": "[{'name': 'Module 1', 'description': 'Description for module 1'}]",
        "owner_id": "1"
    }

    # Expected response
    expected_response: dict[str, Any] = {
        "message": "Organisation created successfully",
        "Organisation": {
            "id": 4,
            "name": "Example Organisation"
        },
        "modules": [
            {
                "id": 9,
                "name": "Module 1"
            }
        ]
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/org/", expected_response, method="POST", data=request_data)


def create_block_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "block_type": "1",
        "order": "1",
        "block_name": "Sky Question",
        "data": "{}"
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Block created"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/module/lesson/1/block", expected_response, method="POST", data=request_data)


def get_blocks_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, Any] = {
        "blocks": [
            {
                "block_type": 1,
                "block_order": 1,
                "block_name": "Sky Question",
                "data": {}
            },
            {
                "block_type": 2,
                "block_order": 2,
                "block_name": "Sky Text",
                "data": {
                    "text": "The sky is blue"
                }
            },
            {
                "block_type": 3,
                "block_order": 3,
                "block_name": "Sky Video",
                "data": {
                    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                }
            },
            {
                "block_type": 4,
                "block_order": 4,
                "block_name": "Sky Image",
                "data": {
                    "image_url": "https://www.example.com/image.jpg"
                }
            }
        ]
    }

    # Call the API endpoint
    test_endpoint("/v1/module/lesson/1/block", expected_response)


def delete_block_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "block_type": "1",
        "order": "1"
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Block deleted"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/module/lesson/1/block", expected_response, method="DELETE", data=request_data)


def get_module_lessons_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, Any] = {
        "lessons": [
            {
                "id": 1,
                "title": "Introduction",
            },
            {
                "id": 2,
                "title": "Lesson 1",
            },
            {
                "id": 3,
                "title": "Lesson 2",
            },
            {
                "id": 4,
                "title": "Lesson 3",
            }
        ]
    }

    # Call the API endpoint
    test_endpoint("/v1/module/1/lessons", expected_response)


def create_lesson_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "lesson_id": "1",
        "module_id": "1",
        "title": "example_title",
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Lesson created"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/module/lesson/", expected_response, method="POST", data=request_data)


def delete_lesson_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "lesson_id": "1"
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Lesson deleted"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/module/lesson/", expected_response, method="DELETE", data=request_data)


def add_module_subscription_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, Any] = {
        "success": True,
        "message": "Successfully added subscription to user"
    }

    # Call the API endpoint
    test_endpoint("/v1/org/1/module/1/user/1", expected_response, method="PUT")


def get_module_info_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, Any] = {
        "module_id": 1,
        "name": "Personal Development",
        "description": "Learn how to develop yourself",
        "org_id": 1
    }

    # Call the API endpoint
    test_endpoint("/v1/module/1/", expected_response)


def activate_module_code_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "code": "INTRO1"
    }

    # Expected response
    expected_response: dict[str, Any] = {
        "message": "Successfully subscribed user 1 to 3 modules",
        "modules": [1, 2, 3]
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/module/code/1", expected_response, method="PUT", data=request_data)

def verify_email_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "email": "example_user@example.com",
        "token": "123456"
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Bad Request"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/auth/verify-email", expected_response, method="POST", data=request_data)


def username_check_endpoint_test() -> None:
    # Expected response
    expected_response: dict[str, str] = {
        "message": "Valid username"
    }

    # Call the API endpoint with the username parameter
    test_endpoint("/v1/auth/username?username=example_username", expected_response)


def register_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "email": "new_user@example.com",
        "username": "new_username",
        "password": "new_password",
        "accountType": "user"
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Email not verified"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/auth/register", expected_response, method="POST", data=request_data)


def login_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "email": "example_user@example.com",
        "password": "example_password"
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Bad request"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/auth/login", expected_response, method="POST", data=request_data)


def verify_2fa_endpoint_test() -> None:
    # Request data
    request_data: dict[str, str] = {
        "Limited JWT": "Bearer example_limited_jwt",
        "code": "123456"
    }

    # Expected response
    expected_response: dict[str, str] = {
        "message": "Internal Server Error"
    }

    # Call the API endpoint with form data
    test_endpoint("/v1/auth/2fa", expected_response, method="POST", data=request_data)


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
        subscriptions_endpoint_test()
        profile_endpoint_test()
        module_dashboard_endpoint_test()
        dashboard_endpoint_test()
        create_organisation_endpoint_test()
        create_block_endpoint_test()
        get_blocks_endpoint_test()
        delete_block_endpoint_test()
        get_module_lessons_endpoint_test()
        create_lesson_endpoint_test()
        delete_lesson_endpoint_test()
        add_module_subscription_endpoint_test()
        get_module_info_endpoint_test()
        activate_module_code_endpoint_test()
        verify_email_endpoint_test()
        username_check_endpoint_test()
        register_endpoint_test()
        login_endpoint_test()
        print("All tests passed!\n")
    except AssertionError as e:
        input(f"Test failed: {e}")
