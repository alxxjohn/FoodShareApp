from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from foodshareapp.db.utils import db


class FoodbankModel(BaseModel):
    business_id: UUID
    company_name: str
    address: str
    city: str
    state: str
    zipcode: str
    lat: str
    lng: str
    is_foodbank: bool
    assoc_user: UUID


@dataclass
class InventoryModel(BaseModel):
    item_name: str
    item_qty: int
    # expiration_date: Optional[datetime]


@dataclass
class DonationModel(BaseModel):
    donor_id: UUID
    item_name: str
    quantity: int
    donated_at: datetime


async def get_all_foodbanks() -> list[FoodbankModel]:
    """Returns a list of all businesses"""
    query = "SELECT * FROM business"
    rows = await db.fetch_all(query=query)
    return [FoodbankModel(**dict(row)) for row in rows]


async def get_foodbank_inventory(foodbank_id: UUID) -> list[InventoryModel]:
    query = """
        SELECT item_name, item_qty
        FROM inventory
        WHERE foodbank_id = :foodbank_id
    """
    rows = await db.fetch_all(query, values={"foodbank_id": foodbank_id})
    return [InventoryModel(**dict(row)) for row in rows]


async def get_foodbank_donations(foodbank_id: UUID) -> list[DonationModel]:
    query = """
        SELECT donor_id, item_name, quantity, donated_at
        FROM donations
        WHERE foodbank_id = :foodbank_id
        ORDER BY donated_at DESC
    """
    rows = await db.fetch_all(query, values={"foodbank_id": foodbank_id})
    return [DonationModel(**dict(row)) for row in rows]
