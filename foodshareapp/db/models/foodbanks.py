from dataclasses import dataclass
from dataclasses import asdict
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
    is_business: bool
    date_added: datetime


async def get_all_foodbanks() -> list[FoodbankModel]:
    """Returns a list of all users who are foodbanks (is_business = True)"""
    query = "SELECT * FROM foodshare_users WHERE is_business = TRUE"
    rows = await db.fetch_all(query=query)
    return [FoodbankModel(**dict(row)) for row in rows]


async def get_foodbank_inventory(foodbank_id: UUID):
    query = """
        SELECT item_name, quantity, expiration_date
        FROM foodshare_inventory
        WHERE foodbank_id = :foodbank_id
    """
    return await db.fetch_all(query, values={"foodbank_id": foodbank_id})


async def get_foodbank_donations(foodbank_id: UUID):
    query = """
        SELECT donor_id, item_name, quantity, donated_at
        FROM foodshare_donations
        WHERE foodbank_id = :foodbank_id
        ORDER BY donated_at DESC
    """
    return await db.fetch_all(query, values={"foodbank_id": foodbank_id})
