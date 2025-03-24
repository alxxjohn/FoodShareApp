from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class CreateReservation(BaseModel):
    """
    DTO for reservation models.

    returned when accessing reservation models from the API.
    """

    reservationID: UUID
    reservationMadeTime: datetime
    foodbankId: UUID
    itemId: UUID
    itemName: str
    userId: UUID
    itemQty: int
    pickupTime: datetime
    showedUp: bool
    showedUpTime: Optional[datetime]
    status: str


class CreateReservationResponse(CreateReservation):
    reservationID: UUID
    reservationMadeTime: datetime


class DeleteReservation(BaseModel):
    reservationID: UUID


class updateReservationResponse(BaseModel):
    reservationID: UUID
    reservationMadeTime: datetime
    foodbankId: UUID
    itemId: UUID
    userId: UUID
    itemQty: int
    pickupTime: datetime
    showedUp: bool
    showedUpTime: Optional[datetime]
    status: str
