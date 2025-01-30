from psycopg.connection import Connection
from psycopg.rows import TupleRow
from psycopg.cursor import Cursor


def create_user_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
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


def create_organisations_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS organisations (
        orgID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) UNIQUE NOT NULL,
        description VARCHAR(100) NOT NULL,
        ownerID INT REFERENCES users(userID) NOT NULL
    );"""
    )


def create_modules_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS modules (
        moduleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );"""
    )


def create_module_teachers_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS module_teachers (
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        userID INT REFERENCES users(userID) NOT NULL,
        PRIMARY KEY (moduleID, userID)
    );"""
    )


def create_bundles_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS bundles (
        bundleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );"""
    )


def create_bundle_modules_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS bundle_modules (
        bundleID INT REFERENCES bundles(bundleID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (bundleID, moduleID)
    );"""
    )


def create_content_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS content (
        contentID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        title VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        content JSON NOT NULL
    );"""
    )


def create_subscriptions_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS subscriptions (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (userID, moduleID)
    );"""
    )


def create_progress_table(cursor: Cursor[TupleRow]) -> None:
    _ = cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS progress (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        progress JSON NOT NULL
    );"""
    )


def initialise_tables(conn: Connection[TupleRow]) -> None:
    cursor: Cursor[TupleRow] = conn.cursor()
    create_user_table(cursor)
    create_organisations_table(cursor)
    create_modules_table(cursor)
    create_module_teachers_table(cursor)
    create_bundles_table(cursor)
    create_bundle_modules_table(cursor)
    create_content_table(cursor)
    create_subscriptions_table(cursor)
    create_progress_table(cursor)
    conn.commit()
