import pytest
import sqlite3


@pytest.fixture(scope="session")
def test_database():
    """Creates an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE foodshare_users (
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

    cursor.executemany(
        "INSERT INTO foodshare_users VALUES(?, ?, ?, ?, ?, ?, ?)", sample_data
    )
    conn.commit()

    yield conn
    conn.close()


def test_register_new_user(test_database):
    """Test registering a new user."""
    cursor = test_database.cursor()

    # New user data
    new_user = (
        "12345678-1234-1234-1234-123456789abc",
        "newregister@test.com",
        "newuser",
        "New",
        "Register",
        "newpassword",
        1,
    )

    cursor.execute("INSERT INTO foodshare_users VALUES(?, ?, ?, ?, ?, ?, ?)", new_user)
    test_database.commit()

    cursor.execute(
        "SELECT * FROM foodshare_users WHERE email = ?", ("newregister@test.com",)
    )
    user = cursor.fetchone()

    assert user is not None
    assert user[1] == "newregister@test.com"


def test_register_duplicate_email(test_database):
    """Test registering a user with a duplicate email."""
    cursor = test_database.cursor()

    duplicate_user = (
        "87654321-4321-4321-4321-987654321abc",
        "alex@test.com",
        "duplicateuser",
        "Duplicate",
        "User",
        "duplicatepassword",
        1,
    )

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO foodshare_users VALUES(?, ?, ?, ?, ?, ?, ?)", duplicate_user
        )
        test_database.commit()


def test_register_missing_fields(test_database):
    """Test registering a user with missing required fields."""
    cursor = test_database.cursor()

    incomplete_user = (
        "11111111-1111-1111-1111-111111111111",
        None,  # Missing email
        "incompleteuser",
        "Incomplete",
        "User",
        "password",
        1,
    )

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO foodshare_users VALUES(?, ?, ?, ?, ?, ?, ?)", incomplete_user
        )
        test_database.commit()
