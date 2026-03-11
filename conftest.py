import os
import sqlite3

import pytest


TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "recipe_test.db")


@pytest.fixture(scope="session", autouse=True)
def _create_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    conn = sqlite3.connect(TEST_DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute(
        """
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """
    )

    conn.commit()
    conn.close()
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture
def db_connection():
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("BEGIN")
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()
