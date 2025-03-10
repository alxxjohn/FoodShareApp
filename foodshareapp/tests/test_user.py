import pytest
import sqlite3


@pytest.fixture(scope="session")
def test_database():
    """Creates an in-memo db for testing."""
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


def test_database_connection(test_database):
    """Test that the database connection is working."""
    cursor = test_database.cursor()
    cursor.execute("SELECT COUNT(*) FROM foodshare_users")
    count = cursor.fetchone()[0]

    assert count == 2


def test_get_user_by_uuid(test_database):
    """Test retrieving a user by UUID."""
    cursor = test_database.cursor()

    target_uuid = "ba177717-21c0-4744-b081-d9d575d4e1d8"

    cursor.execute("SELECT * FROM foodshare_users WHERE uuid = ?", (target_uuid,))
    user = cursor.fetchone()

    assert user is not None
    assert user[0] == target_uuid
    assert user[1] == "alex@test.com"
    assert user[2] == "alex1"
    assert user[3] == "Alex"
    assert user[4] == "TestLast"
    assert user[5] == "hashedpassword"
    assert user[6] == 1


def test_insert_user(test_database):
    """Test inserting a new user into the database."""
    cursor = test_database.cursor()

    new_user = (
        "12345678-1234-1234-1234-123456789abc",
        "newuser@test.com",
        "newuser",
        "Test",
        "User",
        "newpassword",
        1,
    )
    cursor.execute("INSERT INTO foodshare_users VALUES(?, ?, ?, ?, ?, ?, ?)", new_user)
    test_database.commit()

    cursor.execute("SELECT COUNT(*) FROM foodshare_users")
    count = cursor.fetchone()[0]

    assert count == 3


def test_retrieve_user(test_database):
    """Test retrieving a user by email."""
    cursor = test_database.cursor()

    cursor.execute("SELECT * FROM foodshare_users WHERE email = ?", ("alex@test.com",))
    user = cursor.fetchone()

    assert user is not None
    assert user[1] == "alex@test.com"


def test_unique_email_constraint(test_database):
    """Test that inserting a duplicate email fails."""
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


def test_delete_user(test_database):
    """Test deleting a user from the database."""
    cursor = test_database.cursor()

    cursor.execute("DELETE FROM foodshare_users WHERE email = ?", ("alex@test.com",))
    test_database.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM foodshare_users WHERE email = ?", ("alex@test.com",)
    )
    count = cursor.fetchone()[0]

    assert count == 0
