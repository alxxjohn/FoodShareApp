from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, validator
import json

from foodshareapp.db.utils import db
from foodshareapp.db.models.inventory import db as inventory_db


class DonationItemResponse(BaseModel):
    item_id: UUID
    item_name: str
    item_qty: int


class Donation(BaseModel):
    donation_id: UUID
    donation_creation_date: datetime
    foodbank_id: UUID
    donations_array: List[DonationItemResponse]

    @validator("donation_creation_date", pre=True, always=True)
    def ensure_utc(cls, v):
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class CreateDonation:
    donationsArray: List[DonationItemResponse]


class CreateDonationResponse(Donation):
    donation_id: UUID
    donation_creation_date: datetime
    foodbank_id: UUID
    donations_array: List[DonationItemResponse]


class DeleteDonation(BaseModel):
    donation_id: UUID


async def get_foodbank_id_for_user(assoc_user: UUID) -> UUID:
    stmt = """
        SELECT business_id FROM business
        WHERE assoc_user = :assoc_user AND is_foodbank = true
    """
    record = await db.fetch_one(stmt, values={"assoc_user": assoc_user})
    if record is None:
        raise ValueError("Failed to insert donation")
    return record["business_id"]


async def get_donation_by_id(donation_id: UUID) -> Optional[Donation]:
    stmt = "SELECT * FROM donations WHERE donation_id = :donation_id"
    record = await db.fetch_one(stmt, values={"donation_id": donation_id})
    if record is None:
        return None

    record_dict = dict(record)

    record_dict["donations_array"] = [
        DonationItemResponse(**json.loads(item))
        for item in record_dict["donations_array"]
    ]

    return Donation(**record_dict)


async def insert_donation(donation: Donation) -> CreateDonationResponse:
    stmt = """
        INSERT INTO donations (
            donation_id, donation_creation_date, foodbank_id,
            donations_array
        )
        VALUES (
            :donation_id, :donation_creation_date, :foodbank_id,
            :donations_array
        )
    """
    await db.execute(
        stmt,
        values={
            "donation_id": donation.donation_id,
            "donation_creation_date": donation.donation_creation_date,
            "foodbank_id": donation.foodbank_id,
            "donations_array": [
                json.dumps(item.dict(), default=str)
                for item in donation.donations_array
            ],
        },
    )
    return CreateDonationResponse(**donation.dict())


async def delete_donation(donation_id: UUID) -> UUID:
    stmt = "DELETE FROM donations WHERE donation_id = :donation_id"
    await db.execute(stmt, values={"donation_id": donation_id})
    return donation_id


async def upsert_inventory_item(
    foodbank_id: UUID, item_id: UUID, item_name: str, item_qty: int
):
    """
    Inserts or updates an inventory item for a foodbank.
    """
    check_stmt = """
        SELECT item_qty FROM inventory
        WHERE foodbank_id = :foodbank_id AND item_id = :item_id
    """
    inventory_record = await inventory_db.fetch_one(
        check_stmt,
        values={"foodbank_id": foodbank_id, "item_id": item_id},
    )

    if inventory_record:
        update_stmt = """
            UPDATE inventory
            SET item_qty = item_qty + :item_qty, item_status = 'available'
            WHERE foodbank_id = :foodbank_id AND item_id = :item_id
        """
        await inventory_db.execute(
            update_stmt,
            values={
                "item_qty": item_qty,
                "foodbank_id": foodbank_id,
                "item_id": item_id,
            },
        )
    else:
        insert_stmt = """
            INSERT INTO inventory (
                foodbank_id, item_id, item_name, item_qty, item_status
            )
            VALUES (
                :foodbank_id, :item_id, :item_name, :item_qty, 'available'
            )
        """
        await inventory_db.execute(
            insert_stmt,
            values={
                "foodbank_id": foodbank_id,
                "item_id": item_id,
                "item_name": item_name,
                "item_qty": item_qty,
            },
        )
