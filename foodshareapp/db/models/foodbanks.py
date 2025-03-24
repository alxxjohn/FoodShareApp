from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from foodshareapp.db.utils import db


@dataclass
class FoodbankModel(BaseModel):
    foodbank_id: UUID
    company_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    date_added: datetime


@dataclass
class InventoryModel(BaseModel):
    item_name: str
    quantity: int
    expiration_date: Optional[datetime]


@dataclass
class DonationModel(BaseModel):
    donor_id: UUID
    item_name: str
    quantity: int
    donated_at: datetime


async def get_all_foodbanks() -> list[FoodbankModel]:
    """Returns a list of all users who are foodbanks (is_business = True)"""
    query = "SELECT * FROM users WHERE is_business = TRUE"
    rows = await db.fetch_all(query=query)
    return [FoodbankModel(**dict(row)) for row in rows]


async def get_foodbank_inventory(foodbank_id: UUID) -> list[InventoryModel]:
    query = """
        SELECT item_name, quantity, expiration_date
        FROM inventory
        WHERE foodbank_id = :foodbank_id
    """
    return await db.fetch_all(query, values={"foodbank_id": foodbank_id})


async def get_foodbank_donations(foodbank_id: UUID) -> list[DonationModel]:
    query = """
        SELECT donor_id, item_name, quantity, donated_at
        FROM donations
        WHERE foodbank_id = :foodbank_id
        ORDER BY donated_at DESC
    """
    return await db.fetch_all(query, values={"foodbank_id": foodbank_id})
