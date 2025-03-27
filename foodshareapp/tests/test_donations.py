import pytest
import sqlite3
from uuid import uuid4
from datetime import datetime


@pytest.fixture(scope="session")
def test_database():
    """Creates a db with a donations table for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE donations (
            donationID TEXT PRIMARY KEY,
            donationDate TEXT,
            businessID TEXT,
            foodbankID TEXT,
            donationWeight INTEGER,
            donationDolAmt REAL,
            donationsArray TEXT
        );
        """
    )

    sample_data = [
        (
            str(uuid4()),
            datetime.utcnow().isoformat(),
            str(uuid4()),
            str(uuid4()),
            100,
            250.00,
            '["' + str(uuid4()) + '", "' + str(uuid4()) + '"]',
        )
    ]

    cursor.executemany(
        """
        INSERT INTO donations
        (donationID, donationDate, businessID, foodbankID,
         donationWeight, donationDolAmt, donationsArray)
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

    new_donation = (
        str(uuid4()),
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        75,
        180.00,
        '["' + str(uuid4()) + '"]',
    )

    cursor.execute(
        """
        INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        new_donation,
    )
    test_database.commit()

    cursor.execute("SELECT * FROM donations WHERE donationDolAmt = ?", (180.00,))
    donation = cursor.fetchone()

    assert donation is not None
    assert donation[5] == 180.00


def test_duplicate_donation_id(test_database):
    """Test inserting a donation with a duplicate donationID."""
    cursor = test_database.cursor()

    donation_id = str(uuid4())

    donation = (
        donation_id,
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        20,
        90.00,
        '["' + str(uuid4()) + '"]',
    )

    cursor.execute("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)", donation)
    test_database.commit()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)", donation)
        test_database.commit()


def test_update_donation_weight(test_database):
    """Test updating the donationWeight of a donation."""
    cursor = test_database.cursor()

    cursor.execute("SELECT donationID FROM donations LIMIT 1")
    donation_id = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE donations SET donationWeight = ? WHERE donationID = ?",
        (200, donation_id),
    )
    test_database.commit()

    cursor.execute(
        "SELECT donationWeight FROM donations WHERE donationID = ?", (donation_id,)
    )
    updated_weight = cursor.fetchone()[0]

    assert updated_weight == 200


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
        55,
        110.00,
        '["' + str(uuid4()) + '"]',
    )
    cursor.execute("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)", donation)
    test_database.commit()

    cursor.execute("DELETE FROM donations WHERE donationID = ?", (donation_id,))
    test_database.commit()

    cursor.execute("SELECT * FROM donations WHERE donationID = ?", (donation_id,))
    deleted = cursor.fetchone()

    assert deleted is None
