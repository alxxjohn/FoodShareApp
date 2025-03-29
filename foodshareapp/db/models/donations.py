from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel
import json

from foodshareapp.db.utils import db
from foodshareapp.db.models.inventory import db as inventory_db


@dataclass
class DonationItemResponse(BaseModel):
    itemId: UUID
    itemName: str
    itemQty: int


@dataclass
class Donation(BaseModel):
    donationID: UUID
    donationMadeTime: datetime
    foodbankId: UUID
    userId: UUID
    donationsArray: List[DonationItemResponse]
    pickupTime: datetime
    status: str


@dataclass
class CreateDonation:
    businessID: UUID
    foodbankID: UUID
    donationWeight: int
    donationDolAmt: float
    donationsArray: List[DonationItemResponse]


@dataclass
class CreateDonationResponse(Donation):
    donationID: UUID
    donationDate: datetime
    businessID: UUID
    foodbankID: UUID
    donationWeight: int
    donationDolAmt: float
    donationsArray: List[DonationItemResponse]


@dataclass
class DeleteDonation(BaseModel):
    donationID: UUID


async def get_donation_by_id(donationID: UUID) -> Optional[Donation]:
    stmt = "SELECT * FROM donations WHERE donationID = :donationID"
    record = await db.fetch_one(stmt, values={"donationID": donationID})
    if record is None:
        return None

    record_dict = dict(record)
    record_dict["donationsArray"] = json.loads(record_dict["donationsArray"])
    return Donation(**record_dict)


async def insert_donation(donation: Donation) -> CreateDonationResponse:
    stmt = """
        INSERT INTO donations (
            donationID, donationMadeTime, foodbankId, userId,
            donationsArray, pickupTime, status
        )
        VALUES (
            :donationID, :donationMadeTime, :foodbankId, :userId,
            :donationsArray, :pickupTime, :status
        )
    """
    await db.execute(
        stmt,
        values={
            "donationID": donation.donationID,
            "donationMadeTime": donation.donationMadeTime,
            "foodbankId": donation.foodbankId,
            "userId": donation.userId,
            "donationsArray": json.dumps(donation.donationsArray),
            "pickupTime": donation.pickupTime,
            "status": donation.status,
        },
    )

    return CreateDonationResponse(**donation.dict())


async def delete_donation(donationID: UUID) -> UUID:
    stmt = "DELETE FROM donations WHERE donationID = :donationID"
    await db.execute(stmt, values={"donationID": donationID})
    return donationID


async def upsert_inventory_item(
    foodbank_id: UUID, item_id: UUID, item_name: str, item_qty: int
):
    """
    Inserts or updates an inventory item for a foodbank.
    """
    check_stmt = """
        SELECT itemQty FROM inventory
        WHERE foodbankId = :foodbankId AND itemId = :itemId
    """
    inventory_record = await inventory_db.fetch_one(
        check_stmt,
        values={"foodbankId": foodbank_id, "itemId": item_id},
    )

    if inventory_record:
        update_stmt = """
            UPDATE inventory
            SET itemQty = itemQty + :qty, itemStatus = 'available'
            WHERE foodbankId = :foodbankId AND itemId = :itemId
        """
        await inventory_db.execute(
            update_stmt,
            values={
                "qty": item_qty,
                "foodbankId": foodbank_id,
                "itemId": item_id,
            },
        )
    else:
        insert_stmt = """
            INSERT INTO inventory (
                inventoryID, foodbankId, itemId, itemName, itemQty, itemStatus
            )
            VALUES (
                :inventoryID, :foodbankId, :itemId, :itemName, :qty, 'available'
            )
        """
        await inventory_db.execute(
            insert_stmt,
            values={
                "inventoryID": uuid4(),
                "foodbankId": foodbank_id,
                "itemId": item_id,
                "itemName": item_name,
                "qty": item_qty,
            },
        )
