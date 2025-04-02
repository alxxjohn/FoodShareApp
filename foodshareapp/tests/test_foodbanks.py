import pytest
import sqlite3
from uuid import uuid4
from datetime import datetime


@pytest.fixture(scope="session")
def test_foodbanks_database():
    """Creates in-memory tables for foodbanks, inventory, and donations."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE users (
            uuid TEXT PRIMARY KEY,
            email TEXT,
            username TEXT,
            firstname TEXT,
            lastname TEXT,
            company_name TEXT,
            address TEXT,
            phone TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            is_business BOOL
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE inventory (
            foodbankID TEXT,
            itemID TEXT,
            itemName TEXT,
            itemQuant INTEGER
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE donations (
            donationID TEXT PRIMARY KEY,
            businessID TEXT,
            foodBankID TEXT,
            donationDate TEXT,
            donationWeight INTEGER,
            donationDolAmt FLOAT,
            itemID TEXT,
            itemAmount INTEGER
        );
    """
    )

    foodbank_id = str(uuid4())
    cursor.execute(
        """
        INSERT INTO users (uuid, email, username, firstname, lastname, company_name, address, phone, city, state, zip, is_business)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    """,
        (
            foodbank_id,
            "bank@example.com",
            "foodbank",
            "Jane",
            "Doe",
            "Helping Hands",
            "123 Main St",
            "123-456-7890",
            "New York",
            "NY",
            "10001",
        ),
    )

    cursor.execute(
        """
        INSERT INTO inventory (foodbankID, itemID, itemName, itemQuant)
        VALUES (?, ?, ?, ?)
    """,
        (foodbank_id, str(uuid4()), "Canned Soup", 50),
    )

    cursor.execute(
        """
        INSERT INTO donations (donationID, businessID, foodBankID, donationDate, donationWeight, donationDolAmt, itemID, itemAmount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            str(uuid4()),
            str(uuid4()),
            foodbank_id,
            datetime.utcnow().isoformat(),
            100,
            500.0,
            str(uuid4()),
            10,
        ),
    )

    conn.commit()
    yield conn
    conn.close()


def test_get_foodbanks(test_foodbanks_database):
    cursor = test_foodbanks_database.cursor()
    cursor.execute("SELECT * FROM users WHERE is_business = 1")
    foodbanks = cursor.fetchall()

    assert len(foodbanks) > 0
    assert foodbanks[0][2] == "foodbank"  # username


def test_get_foodbank_inventory(test_foodbanks_database):
    cursor = test_foodbanks_database.cursor()
    cursor.execute("SELECT * FROM inventory WHERE itemName = 'Canned Soup'")
    item = cursor.fetchone()

    assert item is not None
    assert item[2] == "Canned Soup"  # itemName
    assert item[3] == 50  # itemQty


def test_get_foodbank_donations(test_foodbanks_database):
    cursor = test_foodbanks_database.cursor()
    cursor.execute("SELECT * FROM donations")
    donation = cursor.fetchone()

    assert donation is not None
    assert donation[4] == 100
    assert donation[5] == 500.0
