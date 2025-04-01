from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List


class DonationItem(BaseModel):
    item_name: str
    item_qty: int


class CreateDonation(BaseModel):
    donations_array: List[DonationItem]


class DonationItemResponse(BaseModel):
    item_id: UUID
    item_name: str
    item_qty: int


class Donation(BaseModel):
    """
    DTO for donation models.

    returned when accessing donation models from the API.
    """

    donation_id: UUID
    donation_creation_date: datetime
    foodbank_id: UUID
    donations_array: List[DonationItemResponse]


class CreateDonationResponse(CreateDonation):
    donation_id: UUID
    donation_creation_date: datetime
    foodbank_id: UUID
    donations_array: List[DonationItem]


class DeleteDonation(BaseModel):
    donation_id: UUID


class UpdateDonationResponse(BaseModel):
    donation_id: UUID
    donation_creation_date: datetime
    foodbank_id: UUID
    donations_array: List[DonationItemResponse]
