import pytest
import sqlite3


@pytest.fixture(scope="session")
def test_database():
    """Creates an in-memory SQLite database for user testing."""
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

    conn.commit()
    yield conn
    conn.close()


def test_register_new_user(test_database):
    cursor = test_database.cursor()

    new_user = (
        "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
        "newuser@example.com",
        "newuser123",
        "Alice",
        "Johnson",
        "random_salt_value",
        "secure_hashed_password",
        True,
        "2025-03-10 10:30:00",
        None,
        None,
        0,
        False,
        True,
        "2025-03-10 10:35:00",
        "Tech Solutions Inc.",
        "789 Maple Ave",
        "Chicago",
        "IL",
        "60616",
        "555-9876",
        False,
        False,
    )

    cursor.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        new_user,
    )
    test_database.commit()

    cursor.execute("SELECT * FROM users WHERE email = ?", ("newuser@example.com",))
    user = cursor.fetchone()

    assert user is not None
    assert user[1] == "newuser@example.com"


def test_register_duplicate_email(test_database):
    cursor = test_database.cursor()

    existing_user = (
        "11111111-2222-3333-4444-555555555555",
        "duplicate@example.com",
        "existinguser",
        "Alex",
        "User",
        "random_salt",
        "existingpassword",
        1,
        "2025-03-10 12:00:00",
        None,
        None,
        0,
        0,
        1,
        "2025-03-10 12:05:00",
        "Existing Company",
        "123 Test St",
        "Test City",
        "TX",
        "75001",
        "555-9999",
        0,
        0,
    )

    cursor.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        existing_user,
    )
    test_database.commit()

    duplicate_user = (
        "87654321-4321-4321-4321-987654321abc",
        "duplicate@example.com",
        "duplicateuser",
        "Duplicate",
        "User",
        "random_salt",
        "duplicatepassword",
        1,
        "2025-03-10 12:00:00",
        None,
        None,
        0,
        0,
        1,
        "2025-03-10 12:05:00",
        "Tech Solutions",
        "123 Test St",
        "Test City",
        "TX",
        "75001",
        "555-9999",
        0,
        0,
    )

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            duplicate_user,
        )
        test_database.commit()


def test_register_missing_fields(test_database):
    cursor = test_database.cursor()

    incomplete_user = (
        "11111111-1111-1111-1111-111111111111",
        None,
        "incompleteuser",
        "Incomplete",
        "User",
        "random_salt",
        "password",
        1,
        "2025-03-10 12:00:00",
        None,
        None,
        0,
        0,
        1,
        None,
        "Missing Inc.",
        "456 Another St",
        "Another City",
        "CA",
        "90210",
        "555-8888",
        1,
        1,
    )

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            incomplete_user,
        )
        test_database.commit()
