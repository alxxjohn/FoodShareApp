import pytest
import sqlite3
from uuid import uuid4
from datetime import datetime


@pytest.fixture(scope="session")
def test_database():
    """Creates a db with a reservations table for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE reservations (
            reservationID TEXT PRIMARY KEY,
            reservationMadeTime TEXT,
            foodbankId TEXT,
            itemId TEXT,
            itemName TEXT,
            userId TEXT,
            itemQty INTEGER,
            pickupTime TEXT,
            showedUp BOOLEAN,
            showedUpTime TEXT,
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
            "Milk",
            str(uuid4()),
            3,
            datetime.utcnow().isoformat(),
            False,
            None,
            "active",
        )
    ]

    cursor.executemany(
        """
        INSERT INTO reservations
        (reservationID, reservationMadeTime, foodbankId, itemId, itemName, userId, itemQty,
         pickupTime, showedUp, showedUpTime, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sample_data,
    )
    conn.commit()
    yield conn
    conn.close()


def test_create_reservation(test_database):
    """Test inserting a new reservation."""
    cursor = test_database.cursor()

    new_reservation = (
        str(uuid4()),
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        "Eggs",
        str(uuid4()),
        2,
        datetime.utcnow().isoformat(),
        False,
        None,
        "active",
    )

    cursor.execute(
        """
        INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        new_reservation,
    )
    test_database.commit()

    cursor.execute("SELECT * FROM reservations WHERE itemName = ?", ("Eggs",))
    reservation = cursor.fetchone()

    assert reservation is not None
    assert reservation[4] == "Eggs"


def test_duplicate_reservation_id(test_database):
    """Test inserting a reservation with a duplicate reservationID."""
    cursor = test_database.cursor()

    reservation_id = str(uuid4())

    reservation = (
        reservation_id,
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        "Bread",
        str(uuid4()),
        1,
        datetime.utcnow().isoformat(),
        False,
        None,
        "active",
    )

    cursor.execute(
        "INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", reservation
    )
    test_database.commit()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            reservation,
        )
        test_database.commit()


def test_update_reservation_status(test_database):
    """Test updating the status of a reservation."""
    cursor = test_database.cursor()

    cursor.execute("SELECT reservationID FROM reservations LIMIT 1")
    reservation_id = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE reservations SET status = ? WHERE reservationID = ?",
        ("completed", reservation_id),
    )
    test_database.commit()

    cursor.execute(
        "SELECT status FROM reservations WHERE reservationID = ?", (reservation_id,)
    )
    updated_status = cursor.fetchone()[0]

    assert updated_status == "completed"


def test_get_nonexistent_reservation(test_database):
    """Test selecting a reservation that doesn't exist."""
    cursor = test_database.cursor()
    fake_id = str(uuid4())

    cursor.execute("SELECT * FROM reservations WHERE reservationID = ?", (fake_id,))
    result = cursor.fetchone()

    assert result is None


def test_get_existing_reservation(test_database):
    """Test selecting an existing reservation by ID."""
    cursor = test_database.cursor()

    cursor.execute("SELECT reservationID FROM reservations LIMIT 1")
    reservation_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT * FROM reservations WHERE reservationID = ?", (reservation_id,)
    )
    reservation = cursor.fetchone()

    assert reservation is not None
    assert reservation[0] == reservation_id


def test_delete_reservation(test_database):
    """Test deleting a reservation by ID."""
    cursor = test_database.cursor()

    reservation_id = str(uuid4())
    reservation = (
        reservation_id,
        datetime.utcnow().isoformat(),
        str(uuid4()),
        str(uuid4()),
        "Cheese",
        str(uuid4()),
        1,
        datetime.utcnow().isoformat(),
        False,
        None,
        "active",
    )
    cursor.execute(
        "INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", reservation
    )
    test_database.commit()

    cursor.execute(
        "DELETE FROM reservations WHERE reservationID = ?", (reservation_id,)
    )
    test_database.commit()

    cursor.execute(
        "SELECT * FROM reservations WHERE reservationID = ?", (reservation_id,)
    )
    deleted = cursor.fetchone()

    assert deleted is None
