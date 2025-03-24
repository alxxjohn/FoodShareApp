import pytest
import sqlite3


@pytest.fixture(scope="session")
def test_database():
    """Creates an db for testing."""
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

    sample_data = [
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
            "2c38e819-d4da-4e75-965d-dd9b2834e329",
            "other@test.com",
            "test1",
            "Test",
            "User",
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
            "Other Business",
            "456 Another St",
            "Another City",
            "CA",
            "90210",
            "555-5678",
            1,
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
        sample_data,
    )
    conn.commit()

    yield conn
    conn.close()


def test_register_new_user(test_database):
    """Test registering a new user."""
    cursor = test_database.cursor()

    new_user = (
        "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
        "newuser@example.com",  # Correct email
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

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        ("newuser@example.com",),  # Correct email in SELECT query
    )
    user = cursor.fetchone()

    assert user is not None, "User should be found in the database"
    assert user[1] == "newuser@example.com"


def test_register_duplicate_email(test_database):
    """Test registering a user with a duplicate email."""
    cursor = test_database.cursor()

    # Ensure "alex@test.com" does not exist before inserting
    cursor.execute("DELETE FROM users WHERE email = ?", ("alex@test.com",))
    test_database.commit()

    existing_user = (
        "11111111-2222-3333-4444-555555555555",
        "alex@test.com",
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
        "alex@test.com",  # Duplicate email
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
            """
            INSERT INTO users (uuid, email, username, firstname, lastname, salt, password,
                               tos_accepted, tos_accepted_date, last_login, bad_login_attempt,
                               bad_login_count, account_locked, account_verified, account_verified_at,
                               company_name, address, city, state, zip, phone, is_business, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            duplicate_user,
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
        "random_salt",
        "password",
        1,
        "2025-03-10 12:00:00",
        None,
        None,
        0,
        0,
        1,
        None,  # Missing account_verified_at
        "Alex's Business",
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
            """
            INSERT INTO users
            (uuid, email, username, firstname, lastname, salt, password,
             tos_accepted, tos_accepted_date, last_login, bad_login_attempt,
             bad_login_count, account_locked, account_verified, account_verified_at,
             company_name, address, city, state, zip, phone, is_business, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            incomplete_user,
        )
        test_database.commit()


def test_register_business_user(test_database):
    """Test registering a business user with a company name but no first and last name."""
    cursor = test_database.cursor()

    business_user = (
        "99999999-8888-7777-6666-555555555555",
        "business@test.com",
        "businessuser",
        None,  # No first name
        None,  # No last name
        "random_salt",
        "secure_hashed_password",
        1,
        "2025-03-10 12:00:00",
        None,
        None,
        0,
        0,
        1,
        "2025-03-10 12:05:00",
        "Tech Corp",  # Company name provided
        "789 Business St",
        "Business City",
        "CA",
        "90210",
        "555-4321",
        1,  # is_business = True
        0,  # is_admin = False
    )

    cursor.execute(
        """
        INSERT INTO users (uuid, email, username, firstname, lastname, salt, password,
                           tos_accepted, tos_accepted_date, last_login, bad_login_attempt,
                           bad_login_count, account_locked, account_verified, account_verified_at,
                           company_name, address, city, state, zip, phone, is_business, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        business_user,
    )
    test_database.commit()

    cursor.execute(
        "SELECT company_name, firstname, lastname FROM users WHERE email = ?",
        ("business@test.com",),
    )
    user = cursor.fetchone()

    assert user is not None, "Business user should be found in the database"
    assert (
        user[0] == "Tech Corp"
    ), f"Expected company_name to be 'Tech Corp', got '{user[0]}'"
    assert user[1] is None, f"Expected firstname to be NULL, got '{user[1]}'"
    assert user[2] is None, f"Expected lastname to be NULL, got '{user[2]}'"


def test_register_admin_user(test_database):
    """Test registering an admin user."""
    cursor = test_database.cursor()

    admin_user = (
        "55555555-6666-7777-8888-999999999999",
        "admin@test.com",
        "adminuser",
        "Admin",
        "User",
        "random_salt",
        "secure_hashed_password",
        1,
        "2025-03-10 12:00:00",
        None,
        None,
        0,
        0,
        1,
        "2025-03-10 12:05:00",
        None,  # No company name
        "999 Admin St",
        "Admin City",
        "NY",
        "10001",
        "555-0000",
        0,  # is_business = False
        1,  # is_admin = True
    )

    cursor.execute(
        """
        INSERT INTO users (uuid, email, username, firstname, lastname, salt, password,
                           tos_accepted, tos_accepted_date, last_login, bad_login_attempt,
                           bad_login_count, account_locked, account_verified, account_verified_at,
                           company_name, address, city, state, zip, phone, is_business, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        admin_user,
    )
    test_database.commit()
    cursor.execute(
        "SELECT email, is_admin FROM users WHERE email = ?", ("admin@test.com",)
    )
    user = cursor.fetchone()

    assert user is not None, "Admin user should be found in the database"
    assert user[1] == 1, f"Expected is_admin to be 1, got '{user[1]}'"
