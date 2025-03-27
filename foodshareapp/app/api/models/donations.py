from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List


class DonationItem(BaseModel):
    itemName: str
    itemQty: int


class CreateDonation(BaseModel):
    foodbankId: UUID
    donationsArray: List[DonationItem]


class DonationItemResponse(BaseModel):
    itemId: UUID
    itemName: str
    itemQty: int


class Donation(BaseModel):
    """
    DTO for donation models.

    returned when accessing donation models from the API.
    """

    donationID: UUID
    donationMadeTime: datetime
    foodbankId: UUID
    userId: UUID
    donationsArray: List[DonationItemResponse]
    pickupTime: datetime
    status: str


class CreateDonationResponse(CreateDonation):
    donationID: UUID
    donationMadeTime: datetime
    userId: UUID
    donationsArray: List[DonationItem]
    status: str


class DeleteDonation(BaseModel):
    donationID: UUID


class UpdateDonationResponse(BaseModel):
    donationID: UUID
    donationMadeTime: datetime
    foodbankId: UUID
    donationsArray: List[DonationItemResponse]
    userId: UUID
    pickupTime: datetime
    status: str
