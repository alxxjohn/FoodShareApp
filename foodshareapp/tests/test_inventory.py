import pytest
import sqlite3
from uuid import uuid4
from datetime import datetime


@pytest.fixture(scope="session")
def test_inventory_database():
    """Creates an in-memory inventory table for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE inventory (
            inventoryID TEXT PRIMARY KEY,
            foodbankId TEXT,
            itemId TEXT,
            itemName TEXT,
            itemQty INTEGER,
            date_added TEXT,
            status TEXT
        );
        """
    )

    sample_inventory = [
        (
            str(uuid4()),
            str(uuid4()),
            str(uuid4()),
            "Rice",
            10,
            datetime.utcnow().isoformat(),
            "donated",
        )
    ]

    cursor.executemany(
        """
        INSERT INTO inventory
        (inventoryID, foodbankId, itemId, itemName, itemQty, date_added, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        sample_inventory,
    )

    conn.commit()
    yield conn
    conn.close()


def test_create_inventory_item(test_inventory_database):
    """Test inserting a new inventory item."""
    cursor = test_inventory_database.cursor()

    new_inventory = (
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        "Beans",
        5,
        datetime.utcnow().isoformat(),
        "donated",
    )

    cursor.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?, ?)", new_inventory)
    test_inventory_database.commit()

    cursor.execute("SELECT * FROM inventory WHERE itemName = ?", ("Beans",))
    result = cursor.fetchone()

    assert result is not None
    assert result[3] == "Beans"


def test_update_inventory_quantity(test_inventory_database):
    """Test updating the quantity of an inventory item."""
    cursor = test_inventory_database.cursor()

    cursor.execute("SELECT inventoryID FROM inventory LIMIT 1")
    inventory_id = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE inventory SET itemQty = itemQty - 2 WHERE inventoryID = ?",
        (inventory_id,)
    )
    test_inventory_database.commit()

    cursor.execute(
        "SELECT itemQty FROM inventory WHERE inventoryID = ?", (inventory_id,)
    )
    updated_qty = cursor.fetchone()[0]

    assert updated_qty == 8


def test_get_existing_inventory_item(test_inventory_database):
    """Test selecting an existing inventory item by ID."""
    cursor = test_inventory_database.cursor()

    cursor.execute("SELECT inventoryID FROM inventory LIMIT 1")
    inventory_id = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM inventory WHERE inventoryID = ?", (inventory_id,))
    item = cursor.fetchone()

    assert item is not None
    assert item[0] == inventory_id


def test_delete_inventory_item(test_inventory_database):
    """Test deleting an inventory item by ID."""
    cursor = test_inventory_database.cursor()

    inventory_id = str(uuid4())
    inventory = (
        inventory_id,
        str(uuid4()),
        str(uuid4()),
        "Flour",
        3,
        datetime.utcnow().isoformat(),
        "donated",
    )
    cursor.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?, ?)", inventory)
    test_inventory_database.commit()

    cursor.execute("DELETE FROM inventory WHERE inventoryID = ?", (inventory_id,))
    test_inventory_database.commit()

    cursor.execute("SELECT * FROM inventory WHERE inventoryID = ?", (inventory_id,))
    deleted = cursor.fetchone()

    assert deleted is None


def test_get_nonexistent_inventory_item(test_inventory_database):
    """Test selecting an inventory item that doesn't exist."""
    cursor = test_inventory_database.cursor()
    fake_id = str(uuid4())

    cursor.execute("SELECT * FROM inventory WHERE inventoryID = ?", (fake_id,))
    result = cursor.fetchone()

    assert result is None
