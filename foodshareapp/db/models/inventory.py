from dataclasses import dataclass
from dataclasses import asdict
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from foodshareapp.db.utils import db


@dataclass
class Inventory(BaseModel):
    inventoryID: UUID
    foodbankId: UUID
    itemId: UUID
    itemName: str
    itemQty: int
    date_added: datetime
    status: str = "donated"


class CreateInventory(BaseModel):
    foodbankId: UUID
    itemId: UUID
    itemName: str
    itemQty: int
    status: str


@dataclass
class CreateInventoryResponse(Inventory):
    inventoryID: UUID
    date_added: datetime


@dataclass
class DeleteInventory(BaseModel):
    inventoryID: UUID


async def get_inventory_by_id(inventoryID: UUID) -> Optional[Inventory]:
    """Get inventory by ID."""

    stmt = "SELECT * FROM inventory WHERE inventoryID = :inventoryID"
    db_inventory = await db.fetch_one(stmt, values={"inventoryID": inventoryID})
    if db_inventory is None:
        return None
    return Inventory(**dict(db_inventory))


async def insert_inventory(inventory: Inventory) -> CreateInventoryResponse:
    """Insert a new inventory."""

    stmt = (
        "INSERT INTO inventory (inventoryID, foodbankId, itemId, itemName, itemQty, date_added, status) "
        "VALUES (:inventoryID, :foodbankId, :itemId, :itemName, :itemQty, :date_added, :status) "
        "RETURNING inventoryID, date_added"
    )
    db_inventory = await db.fetch_one(stmt, values=asdict(inventory))
    if db_inventory is None:
        raise ValueError("Failed to insert inventory")

    return CreateInventoryResponse(**dict(db_inventory))


async def delete_inventory(inventoryID: UUID) -> UUID:
    """Delete an inventory."""

    if await get_inventory_by_id(inventoryID) is None:
        raise ValueError("Inventory not found")

    stmt = "DELETE FROM inventory WHERE inventoryID = :inventoryID"
    await db.execute(stmt, values={"inventoryID": inventoryID})

    return inventoryID


async def list_inventory() -> list[Inventory]:
    """List all inventory items."""
    stmt = "SELECT * FROM inventory"
    db_inventory = await db.fetch_all(stmt)
    return [Inventory(**dict(item)) for item in db_inventory] if db_inventory else []
