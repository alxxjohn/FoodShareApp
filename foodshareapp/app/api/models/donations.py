from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Donation(BaseModel):
    """
    DTO for donation models.

    returned when accessing donation models from the API.
    """

    donationID: UUID
    donationMadeTime: datetime
    foodbankId: UUID
    userId: UUID
    itemId: UUID
    itemName: str
    userId: UUID
    itemQty: int
    pickupTime: datetime
    status: str


class CreateDonation(BaseModel):
    """
    DTO for donation models.
    Input for Endpoint
    returned when accessing donation models from the API.
    """
    foodbankId: UUID
    itemName: str
    itemQty: int


class CreateDonationResponse(CreateDonation):
    donationID: UUID
    donationMadeTime: datetime
    userId: UUID
    itemId: UUID
    itemName: str
    userId: UUID
    itemQty: int 
    status: str


class DeleteDonation(BaseModel):
    donationID: UUID


class UpdateDonationResponse(BaseModel):
    donationID: UUID
    donationMadeTime: datetime
    foodbankId: UUID
    itemId: UUID
    userId: UUID
    itemQty: int
    pickupTime: datetime
    status: str
