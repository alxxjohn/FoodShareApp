import pytest
import sqlite3
from uuid import uuid4
from datetime import datetime
import json


@pytest.fixture(scope="session")
def test_database():
    """Creates a db with a donations table for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE donations (
            donationID TEXT PRIMARY KEY,
            donationMadeTime TEXT,
            foodbankId TEXT,
            userId TEXT,
            donationsArray TEXT,
            pickupTime TEXT,
            status TEXT
        );
        """
    )

    sample_data = [
        (
            str(uuid4()),
            datetime.utcnow().isoformat(),
            str(uuid4()),
            str(uuid4()),
            '[{"itemId": "' + str(uuid4()) + '", "itemName": "Rice", "itemQty": 10}]',
            None,
            "available",
        )
    ]

    cursor.executemany(
        """
        INSERT INTO donations (
            donationID, donationMadeTime, foodbankId, userId,
            donationsArray, pickupTime, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        sample_data,
    )
    conn.commit()
    yield conn
    conn.close()


def test_create_donation(test_database):
    """Test inserting a new donation."""

    cursor = test_database.cursor()

    donations_json = json.dumps(
        [{"itemId": str(uuid4()), "itemName": "Beans", "itemQty": 5}]
    )

    new_donation = (
        str(uuid4()),
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        donations_json,
        None,
        "available",
    )

    cursor.execute(
        """
        INSERT INTO donations (
            donationID, donationMadeTime, foodbankId, userId,
            donationsArray, pickupTime, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        new_donation,
    )
    test_database.commit()

    cursor.execute("SELECT * FROM donations ORDER BY donationMadeTime DESC LIMIT 1")
    donation = cursor.fetchone()

    assert donation is not None

    print("Raw donationsArray:", donation[4])
    items = json.loads(donation[4])
    print("Parsed items:", items)

    assert any(item["itemName"] == "Beans" for item in items)


def test_duplicate_donation_id(test_database):
    """Test inserting a donation with a duplicate donationID."""
    cursor = test_database.cursor()

    donation_id = str(uuid4())
    donation = (
        donation_id,
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        '[{"itemId": "' + str(uuid4()) + '", "itemName": "Oil", "itemQty": 2}]',
        None,
        "available",
    )

    cursor.execute("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)", donation)
    test_database.commit()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)", donation)
        test_database.commit()


def test_get_nonexistent_donation(test_database):
    """Test selecting a donation that doesn't exist."""
    cursor = test_database.cursor()
    fake_id = str(uuid4())

    cursor.execute("SELECT * FROM donations WHERE donationID = ?", (fake_id,))
    result = cursor.fetchone()

    assert result is None


def test_get_existing_donation(test_database):
    """Test selecting an existing donation by ID."""
    cursor = test_database.cursor()

    cursor.execute("SELECT donationID FROM donations LIMIT 1")
    donation_id = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM donations WHERE donationID = ?", (donation_id,))
    donation = cursor.fetchone()

    assert donation is not None
    assert donation[0] == donation_id


def test_delete_donation(test_database):
    """Test deleting a donation by ID."""
    cursor = test_database.cursor()

    donation_id = str(uuid4())
    donation = (
        donation_id,
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        '[{"itemId": "' + str(uuid4()) + '", "itemName": "Milk", "itemQty": 3}]',
        None,
        "available",
    )
    cursor.execute("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)", donation)
    test_database.commit()

    cursor.execute("DELETE FROM donations WHERE donationID = ?", (donation_id,))
    test_database.commit()

    cursor.execute("SELECT * FROM donations WHERE donationID = ?", (donation_id,))
    deleted = cursor.fetchone()

    assert deleted is None
