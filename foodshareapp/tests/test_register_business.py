import pytest
import sqlite3


@pytest.fixture(scope="session")
def test_database():
    """Creates an in-memory SQLite database for testing."""
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
            is_foodbank BOOLEAN NOT NULL DEFAULT 0,
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

    cursor.execute(
        """
        INSERT INTO businesses (BusinessId, companyName, address, city, state, zipCode, lat, lng, is_foodbank, assoc_user)
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


def test_register_foodbank_account(test_database):
    """Test registering a foodbank business account."""
    cursor = test_database.cursor()

    user_id = "foodbank-user-0001"
    business_id = "foodbank-biz-0001"

    user = (
        user_id,
        "foodbank@example.com",
        "foodbankuser",
        "Food",
        "Bank",
        "salt",
        "pw_hash",
        1,
        "2025-03-10 10:00:00",
        None,
        None,
        0,
        0,
        1,
        "2025-03-10 10:05:00",
        "Helping Hands",
        "100 Charity St",
        "Care City",
        "TX",
        "73301",
        "555-1212",
        1,
        0
    )

    business = (
        business_id,
        "Helping Hands",
        "100 Charity St",
        "Care City",
        "TX",
        "73301",
        "30.2672",
        "-97.7431",
        True,
        user_id
    )

    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user)
    cursor.execute("INSERT INTO businesses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", business)
    test_database.commit()

    cursor.execute("SELECT is_foodbank FROM businesses WHERE BusinessId = ?", (business_id,))
    is_foodbank = cursor.fetchone()[0]
    assert is_foodbank == 1, "Business should be marked as a foodbank"


def test_user_account_locked_status(test_database):
    """Test inserting a user with account_locked = True."""
    cursor = test_database.cursor()

    user = (
        "locked-user-0001",
        "locked@example.com",
        "lockeduser",
        "Locked",
        "Out",
        "salt",
        "pw_hash",
        1,
        "2025-04-01 09:00:00",
        None,
        None,
        0,
        1,
        1,
        "2025-04-01 09:10:00",
        "Locked Co",
        "404 Error Ln",
        "Nowhere",
        "NA",
        "00000",
        "000-0000",
        0,
        0
    )

    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user)
    test_database.commit()

    cursor.execute("SELECT account_locked FROM users WHERE uuid = ?", ("locked-user-0001",))
    locked_status = cursor.fetchone()[0]
    assert locked_status == 1, "User account should be locked"


def test_admin_user_registration(test_database):
    """Test registering an admin user."""
    cursor = test_database.cursor()

    user = (
        "admin-user-0001",
        "admin@example.com",
        "adminuser",
        "Admin",
        "User",
        "salt",
        "pw_hash",
        1,
        "2025-04-01 08:00:00",
        None,
        None,
        0,
        0,
        1,
        "2025-04-01 08:10:00",
        "Admin Co",
        "1 Main St",
        "Capital",
        "DC",
        "20001",
        "123-4567",
        0,
        1
    )

    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user)
    test_database.commit()

    cursor.execute("SELECT is_admin FROM users WHERE uuid = ?", ("admin-user-0001",))
    is_admin = cursor.fetchone()[0]
    assert is_admin == 1, "User should be registered as an admin"
