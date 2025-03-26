from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
import json

from foodshareapp.db.utils import db
from foodshareapp.db.models.inventory import db as inventory_db


@dataclass
class Donation(BaseModel):
    donationID: UUID
    donationDate: datetime
    businessID: UUID
    foodbankID: UUID
    donationWeight: int
    donationDolAmt: float
    donationsArray: List[UUID] 


@dataclass
class CreateDonation:
    businessID: UUID
    foodbankID: UUID
    donationWeight: int
    donationDolAmt: float
    donationsArray: List[UUID]


@dataclass
class CreateDonationResponse(Donation):
    donationID: UUID
    donationDate: datetime
    businessID: UUID
    foodbankID: UUID
    donationWeight: int
    donationDolAmt: float
    donationsArray: List[UUID] 


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
    stmt = (
        "INSERT INTO donations (donationID, donationDate, businessID, foodbankID, "
        "donationWeight, donationDolAmt, donationsArray) "
        "VALUES (:donationID, :donationDate, :businessID, :foodbankID, :donationWeight, "
        ":donationDolAmt, :donationsArray)"
    )

    await db.execute(stmt, values={
        "donationID": donation.donationID,
        "donationDate": donation.donationDate,
        "businessID": donation.businessID,
        "foodbankID": donation.foodbankID,
        "donationWeight": donation.donationWeight,
        "donationDolAmt": donation.donationDolAmt,
        "donationsArray": json.dumps([str(i) for i in donation.donationsArray]),
    })

    for item_id in donation.donationsArray:
        update_qty_stmt = (
            "UPDATE FoodBankInventory SET itemquant = itemquant + 1 "
            "WHERE foodbankID = :foodbankID AND itemID = :itemID"
        )
        await inventory_db.execute(update_qty_stmt, values={
            "foodbankID": donation.foodbankID,
            "itemID": str(item_id)
        })

        update_status_stmt = (
            "UPDATE FoodBankInventory SET itemStatus = 'available' "
            "WHERE foodbankID = :foodbankID AND itemID = :itemID"
        )
        await inventory_db.execute(update_status_stmt, values={
            "foodbankID": donation.foodbankID,
            "itemID": str(item_id)
        })

    return CreateDonationResponse(
        donationID=donation.donationID,
        donationDate=donation.donationDate,
        businessID=donation.businessID,
        foodbankID=donation.foodbankID,
        donationWeight=donation.donationWeight,
        donationDolAmt=donation.donationDolAmt,
        donationsArray=donation.donationsArray,
    )


async def delete_donation(donationID: UUID) -> UUID:
    stmt = "DELETE FROM donations WHERE donationID = :donationID"
    await db.execute(stmt, values={"donationID": donationID})
    return donationID
