import pytest
import sqlite3
from httpx import AsyncClient
from foodshareapp.app.application import app
from foodshareapp.db.utils import db  # Import the actual DB connection


@pytest.fixture(scope="session")
def setup_test_database():
    """Overrides the database connection for testing with SQLite."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            uuid TEXT PRIMARY KEY NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            password TEXT NOT NULL,
            tos_accepted BOOLEAN NOT NULL
        );
    """
    )

    sample_data = [
        (
            "ba177717-21c0-4744-b081-d9d575d4e1d8",
            "alex@test.com",
            "alex1",
            "Alex",
            "TestLast",
            "hashedpassword",
            1,
        ),
        (
            "2c38e819-d4da-4e75-965d-dd9b2834e329",
            "other@test.com",
            "test1",
            "Test",
            "User",
            "hashedpassword",
            1,
        ),
    ]

    cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", sample_data)
    conn.commit()

    db._connection = conn  # Force FastAPI to use SQLite instead of PostgreSQL
    yield conn
    conn.close()


@pytest.fixture(scope="function")
async def client():
    """Provides an async test client for FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
