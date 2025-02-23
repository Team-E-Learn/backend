from psycopg.connection import Connection
from psycopg.rows import TupleRow

# this populates user_ids 1-4 with dummy data
# no alternative API call to add users, so this is the only way to add them
def write_users(conn: Connection[TupleRow]) -> None:
    # format: (accountType, firstName, lastName, username, email)
    users = [
        ('user', 'Alice', 'Smith', 'alice.smith', 'alice.smith@example.com'),
        ('admin', 'Bob', 'Johnson', 'bob.johnson', 'bob.johnson@example.com'),
        ('user', 'Carol', 'Williams', 'carol.williams', 'carol.williams@example.com'),
        ('admin', 'David', 'Brown', 'david.brown', 'david.brown@example.com')
    ]

    with conn.cursor() as cur:
        for accountType, firstName, lastName, username, email in users:
            cur.execute("SELECT 1 FROM users WHERE username = %s OR email = %s", (username, email))
            if cur.fetchone() is None:
                cur.execute(
                    "INSERT INTO users (accountType, firstName, lastName, username, email) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (accountType, firstName, lastName, username, email))


# adds 3 orgs to the DB, user_id 3 is the owner of the first org, user_id 2 is the owner of the other two
# no alternative API call to add organisations, so this is the only way to add them
def write_orgs(conn: Connection[TupleRow]) -> None:
    # format: (name, description, owner_id)
    orgs = [
        ('University of Lincoln', 'A university in Lincoln', 4),
        ('Microsoft', 'A tech company', 2),
        ('Amazon', 'An online retailer', 2)
    ]

    with conn.cursor() as cur:
        for name, description, ownerID in orgs:
            cur.execute("SELECT 1 FROM organisations WHERE name = %s", (name,))
            if cur.fetchone() is None:
                cur.execute(
                    "INSERT INTO organisations (name, description, ownerID) VALUES (%s, %s, %s)",
                    (name, description, ownerID))


# adds 8 modules to the DB, 4 are owned by org_id 1, 2 are owned by org_id 2, 2 are owned by org_id 3
# no alternative API call to add modules, so this is the only way to add them
def write_modules(conn: Connection[TupleRow]) -> None:
    # format: (name, description, org_id)
    modules = [
        ('Personal Development', 'Learn how to develop yourself', 1),
        ('Team Software Engineering', 'Team-based software engineering project', 1),
        ('Networking Fundamentals', 'Basics of networking', 1),
        ('Applied Programming Paradigms', 'Different programming paradigms', 1),
        ('Excel Certification', 'Get certified in Excel', 2),
        ('Advanced Excel', 'Advanced techniques in Excel', 2),
        ('Data Analysis', 'Learn data analysis techniques', 3),
        ('Machine Learning', 'Introduction to machine learning', 3)
    ]

    with conn.cursor() as cur:
        for name, description, orgID in modules:
            cur.execute("SELECT 1 FROM modules WHERE name = %s", (name,))
            if cur.fetchone() is None:
                cur.execute(
                    "INSERT INTO modules (name, description, orgID) VALUES (%s, %s, %s)",
                    (name, description, orgID))


# adds 2 bundles to the DB, each bundle contains a different set of modules
# no alternative API call to add bundles, so this is the only way to add them
def write_bundles(conn: Connection[TupleRow]) -> None:
    # format: (name, description, org_id)
    bundles = [
        ('Computer Science BSc', 'A bundle of modules for a Computer Science degree', 1),
        ('Excel Certification', 'A bundle of modules for an Excel certification', 2)
    ]

    with conn.cursor() as cur:
        for name, description, orgID in bundles:
            cur.execute("SELECT 1 FROM bundles WHERE name = %s", (name,))
            if cur.fetchone() is None:
                cur.execute(
                    "INSERT INTO bundles (name, description, orgID) VALUES (%s, %s, %s)",
                    (name, description, orgID))

        def add_modules_to_bundle(bundle_name, module_names):
            cur.execute("SELECT bundleID FROM bundles WHERE name = %s", (bundle_name,))
            bundle_id = cur.fetchone()[0]
            for module_name in module_names:
                cur.execute("SELECT moduleID FROM modules WHERE name = %s", (module_name,))
                module_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO bundle_modules (bundleID, moduleID) VALUES (%s, %s)",
                    (bundle_id, module_id)
                )

        add_modules_to_bundle('Computer Science BSc', [
            'Team Software Engineering',
            'Networking Fundamentals',
            'Applied Programming Paradigms',
            'Personal Development'
        ])

        add_modules_to_bundle('Excel Certification', [
            'Excel Certification',
            'Advanced Excel'
        ])

# so you don't need to manually add subscriptions with http://127.0.0.1:5000/v1/org/1/module/1/user/1
def write_subscriptions(conn: Connection[TupleRow]) -> None:
    # format: (user_id, module_id)
    subscriptions = [
        (3, 1),
        (3, 2),
        (3, 5),
        (3, 8),
        (4, 1),
        (4, 3),
        (4, 7),
        (4, 8)
    ]

    with conn.cursor() as cur:
        for user_id, module_id in subscriptions:
            cur.execute(
                "INSERT INTO subscriptions (userID, moduleID) VALUES (%s, %s)",
                (user_id, module_id)
            )

# for http://127.0.0.1:5000/v1/user/1/dashboard
# no alternative API call to add dashboard data, so this is the only way to add it
def write_dashboard(conn: Connection[TupleRow]) -> None:
    # format: (user_id, widget_id, widget_type, x, y)
    dashboard = [
        (1, 'announcements_widget', 'announcements', 10, 20),
        (1, 'info_widget', 'info', 30, 20),
        (1, 'about_widget', 'about', 10, 40),
        (1, 'grade_centre_widget', 'grade_centre', 30, 40),
        (1, 'calendar_widget', 'calendar', 10, 60),
        (2, 'announcements_widget', 'announcements', 10, 20),
        (2, 'grade_centre_widget', 'grade_centre', 30, 20),
        (2, 'calendar_widget', 'calendar', 10, 40),
        (3, 'announcements_widget', 'announcements', 10, 20),
        (3, 'info_widget', 'info', 30, 20),
        (3, 'about_widget', 'about', 10, 40),
        (3, 'grade_centre_widget', 'grade_centre', 30, 40),
        (3, 'calendar_widget', 'calendar', 10, 60),
        (4, 'announcements_widget', 'announcements', 10, 20),
        (4, 'grade_centre_widget', 'grade_centre', 30, 20),
        (4, 'calendar_widget', 'calendar', 10, 40)
    ]

    with conn.cursor() as cur:
        for user_id, widget_id, widget_type, x, y in dashboard:
            cur.execute(
                "INSERT INTO dashboard (userID, widgetID, widgetType, x, y) VALUES (%s, %s, %s, %s, %s)",
                (user_id, widget_id, widget_type, x, y)
            )

# for http://127.0.0.1:5000/v1/user/1234/dashboard/module/5678
# no alternative API call to add module dashboard data, so this is the only way to add it
def write_module_dashboard(conn: Connection[TupleRow]) -> None:
    # format: (user_id, module_id, widget_id, widget_type, x, y)
    module_dashboard = [
        (1, 1, 'announcements_widget', 'announcements', 10, 20),
        (1, 1, 'info_widget', 'info', 30, 20),
        (1, 1, 'about_widget', 'about', 10, 40),
        (1, 1, 'grade_centre_widget', 'grade_centre', 30, 40),
        (1, 1, 'calendar_widget', 'calendar', 10, 60),
        (2, 1, 'announcements_widget', 'announcements', 10, 20),
        (2, 1, 'grade_centre_widget', 'grade_centre', 30, 20),
        (2, 1, 'calendar_widget', 'calendar', 10, 40),
        (3, 1, 'announcements_widget', 'announcements', 10, 20),
        (3, 1, 'info_widget', 'info', 30, 20),
        (3, 1, 'about_widget', 'about', 10, 40),
        (3, 1, 'grade_centre_widget', 'grade_centre', 30, 40),
        (3, 1, 'calendar_widget', 'calendar', 10, 60),
        (4, 1, 'announcements_widget', 'announcements', 10, 20),
        (4, 1, 'grade_centre_widget', 'grade_centre', 30, 20),
        (4, 1, 'calendar_widget', 'calendar', 10, 40)
    ]

    with conn.cursor() as cur:
        for user_id, module_id, widget_id, widget_type, x, y in module_dashboard:
            cur.execute(
                "INSERT INTO module_dashboard (userID, moduleID, widgetID, widgetType, x, y) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, module_id, widget_id, widget_type, x, y)
            )