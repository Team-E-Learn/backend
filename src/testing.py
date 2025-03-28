from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement

# todo write tests for each database table, and then each API route

# I'm going to write database testing to check data goes into the DB and comes out the same,
# then I’m also going to check the same read out data can then be read from the API as correct as well.

def write_modules_test(conn: SwapDB) -> None:
    # define modules to write
    # format is (name, description, orgID)
    modules: list[tuple[str, str, int]] = [
        ("Personal Development", "Learn how to develop yourself", 1),
        ("Team Software Engineering", "Team-based software engineering project", 1),
    ]

    # write modules to the database
    cursor: SwapCursor = conn.get_cursor()
    # Write sample modules to the database
    for name, description, orgID in modules:
        result: SwapResult = cursor.execute(
            StringStatement("SELECT 1 FROM modules WHERE name = %s"), (name,)
        )

        if result.fetch_one() is not None:
            # If the module already exists, skip it
            continue

        # Otherwise, add the module to the database
        _ = cursor.execute(
            StringStatement(
                "INSERT INTO modules (name, description, orgID) VALUES (%s, %s, %s)"
            ),
            (name, description, orgID),
        )

    # read modules from the database
    result = cursor.execute(
        StringStatement("SELECT name, description, orgID FROM modules")
    ).fetch_all()

    # compare original and retrieved modules
    assert result == modules, f"Original modules: {modules}, Retrieved modules: {result}"
    print("Module write and read test passed!")
    # todo clean up the database after the test

def write_lessons_test(conn: SwapDB) -> None:
    # define lessons to write
    lessons: list[tuple[int, int, str, str]] = [
        (100, 100, "Test lesson 1", '{"content": "This is test lesson 1"}'),
        (101, 100, "Test lesson 2", '{"content": "This is test lesson 2"}'),
    ]

    # write lessons to the database
    cursor: SwapCursor = conn.get_cursor()
    for lesson_id, module_id, title, description in lessons:
        _ = cursor.execute(
            StringStatement(
                "INSERT INTO lessons (lessonID, moduleID, title, sections) VALUES (%s, %s, %s, %s)"
            ),
            (lesson_id, module_id, title, description),
        )

    # read lessons from the database
    result = cursor.execute(
        StringStatement("SELECT moduleID, title, sections FROM lessons")
    ).fetch_all()

    # compare original and retrieved lessons
    assert result == lessons, f"Original lessons: {lessons}, Retrieved lessons: {result}"
    print("Lesson write and read test passed!")
    # todo clean up the database after the test

def write_block_test(conn: SwapDB) -> None:
    # define blocks to write
    blocks: list[tuple[int, int, int, dict[str, str]]] = [
        (
            100,
            1,
            1,
            {
                "question_content": "Is this a testing block",
                "question_answer": "Yes this is a testing block",
            },
        ),
        (100, 2, 2, {"text": "Second test block"}),
    ]

    # write blocks to the database
    cursor: SwapCursor = conn.get_cursor()
    for lesson_id, block_type, order, data in blocks:
        data = json.dumps(data)
        _ = cursor.execute(
            StringStatement(
                "INSERT INTO blocks (lessonID, blockType, blockOrder, data) VALUES (%s, %s, %s, %s)"
            ),
            (lesson_id, block_type, order, data),
        )

    # read blocks from the database
    result = cursor.execute(StringStatement(
            "SELECT blockType, blockOrder, data FROM blocks WHERE lessonID = 1"
        )
    ).fetch_all()

    # parse the JSON data and recreate blocks list for comparison
    from json import loads
    retrieved_blocks = []
    for block_type, order, data_json in result:
        data_dict = loads(data_json)
        retrieved_blocks.append((1, block_type, order, data_dict))

    # compare original and retrieved blocks
    assert retrieved_blocks == blocks, f"Original blocks: {blocks}, Retrieved blocks: {retrieved_blocks}"
    print("Block write and read test passed!")
    # todo clean up the database after the test


def run_tests(conn: SwapDB) -> None:
    write_modules_test(conn)
    write_lessons_test(conn)
    write_block_test(conn)


