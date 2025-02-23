from psycopg.connection import Connection
from psycopg.rows import TupleRow

# this populates user_ids 1-4 with dummy data
def write_users(conn: Connection[TupleRow]) -> None:
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
def write_orgs(conn: Connection[TupleRow]) -> None:
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
def write_modules(conn: Connection[TupleRow]) -> None:
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
def write_bundles(conn: Connection[TupleRow]) -> None:
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