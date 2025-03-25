import pytest
import sqlite3
from fastapi.testclient import TestClient


from foodshareapp.app.application import app
from foodshareapp.app.api.routes.auth import router as auth_router


app.include_router(auth_router, prefix="/api/auth")

client = TestClient(app)


@pytest.fixture(scope="session")
def test_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE users (
            uuid TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            firstname TEXT,
            lastname TEXT,
            salt TEXT NOT NULL,
            password TEXT NOT NULL,
            tos_accepted BOOLEAN NOT NULL DEFAULT 1,
            tos_accepted_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME,
            bad_login_attempt DATETIME,
            bad_login_count INTEGER,
            account_locked BOOLEAN NOT NULL DEFAULT 0,
            account_verified BOOLEAN DEFAULT 1,
            account_verified_at DATETIME,
            company_name TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            phone TEXT,
            is_business BOOLEAN NOT NULL DEFAULT 0,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        );
        """
    )

    sample_users = [
        (
            "ba177717-21c0-4744-b081-d9d575d4e1d8",
            "alex@test.com",
            "alex1",
            "Alex",
            "TestLast",
            "random_salt",
            "hashedpassword",
            1,
            "2025-03-10 12:00:00",
            None,
            None,
            0,
            0,
            1,
            "2025-03-10 12:05:00",
            "Alex's Business",
            "123 Test St",
            "Test City",
            "TX",
            "75001",
            "555-1234",
            1,
            1,
        ),
        (
            "locked-uuid-user-00000000000000",
            "locked@example.com",
            "lockeduser",
            "Locked",
            "User",
            "salt",
            "hashedpassword",
            1,
            "2025-03-10 12:00:00",
            None,
            None,
            0,
            1,
            1,
            "2025-03-10 12:05:00",
            "Locked Corp",
            "456 Lock St",
            "Lock City",
            "NY",
            "10001",
            "555-0000",
            0,
            0,
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO users
        (uuid, email, username, firstname, lastname, salt, password,
         tos_accepted, tos_accepted_date, last_login, bad_login_attempt,
         bad_login_count, account_locked, account_verified, account_verified_at,
         company_name, address, city, state, zip, phone, is_business, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sample_users,
    )
    conn.commit()

    yield conn
    conn.close()


def test_insert_user_login_data(test_database):
    cursor = test_database.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", ("alex@test.com",))
    user = cursor.fetchone()
    assert user is not None
    assert user[1] == "alex@test.com"
    assert user[12] == 0  # account_locked
    assert user[11] == 0  # bad_login_count


def test_locked_user_login_data(test_database):
    cursor = test_database.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", ("locked@example.com",))
    user = cursor.fetchone()
    assert user is not None
    assert user[12] == 1  # account_locked should be True


def mock_verify_password(input_password, stored_hash, salt):
    # Always return True for testing
    return True


def mock_create_token(uuid):
    return "mocked.jwt.token"
