import pytest
import sqlite3


@pytest.fixture(scope="session")
def test_database():
    """Creates an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create users table
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

    # Create businesses table with lat/lng fields
    cursor.execute(
        """
        CREATE TABLE businesses (
            BusinessId TEXT PRIMARY KEY,
            companyName TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zipCode TEXT NOT NULL,
            lat TEXT,
            lng TEXT,
            isFoodbank BOOLEAN NOT NULL DEFAULT 0,
            assoc_user TEXT NOT NULL
        );
        """
    )

    conn.commit()
    yield conn
    conn.close()


def test_register_business_user_with_linked_business(test_database):
    """Test inserting a business user and creating a linked business entry with lat/lng."""
    cursor = test_database.cursor()

    user_id = "f9f91234-abcd-4d9a-bc23-1234567890ef"
    business_id = "b1234567-890a-4cde-f123-1234567890ab"

    new_user = (
        user_id,
        "linkedbiz@example.com",
        "linkedbizuser",
        "Biz",
        "Linked",
        "saltyhash",
        "pw_hash",
        1,
        "2025-03-25 15:00:00",
        None,
        None,
        0,
        0,
        1,
        "2025-03-25 15:05:00",
        "Linked Biz LLC",
        "500 Linked Way",
        "Link City",
        "FL",
        "33101",
        "555-2222",
        1,
        0,
    )

    new_business = (
        business_id,
        "Linked Biz LLC",
        "500 Linked Way",
        "Link City",
        "FL",
        "33101",
        "25.7617",
        "-80.1918",
        False,
        user_id,
    )

    # Insert user
    cursor.execute(
        """
        INSERT INTO users (uuid, email, username, firstname, lastname, salt, password,
                           tos_accepted, tos_accepted_date, last_login, bad_login_attempt,
                           bad_login_count, account_locked, account_verified, account_verified_at,
                           company_name, address, city, state, zip, phone, is_business, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        new_user,
    )

    # Insert linked business
    cursor.execute(
        """
        INSERT INTO businesses (BusinessId, companyName, address, city, state, zipCode, lat, lng, isFoodbank, assoc_user)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        new_business,
    )

    test_database.commit()

    cursor.execute("SELECT * FROM users WHERE uuid = ?", (user_id,))
    user = cursor.fetchone()
    assert user is not None, "User should be present in users table"
    assert user[1] == "linkedbiz@example.com"

    cursor.execute("SELECT * FROM businesses WHERE assoc_user = ?", (user_id,))
    business = cursor.fetchone()
    assert business is not None, "Business should be present in businesses table"
    assert business[1] == "Linked Biz LLC"
    assert business[6] == "25.7617", f"Expected lat to be 25.7617, got {business[6]}"
    assert business[7] == "-80.1918", f"Expected lng to be -80.1918, got {business[7]}"
    assert business[9] == user_id, "Business should be linked to the correct user"
