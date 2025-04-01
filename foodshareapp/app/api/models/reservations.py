from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CreateReservationItem(BaseModel):
    item_id: UUID
    item_qty: int


class ReservationItem(BaseModel):
    item_id: UUID
    item_name: str
    item_qty: int
    current_status: str


class CreateReservation(BaseModel):
    """
    DTO for reservation models.

    returned when accessing reservation models from the API.
    """

    reserve_time: datetime
    reservations_array: List[CreateReservationItem]


class CreateReservationResponse(BaseModel):
    reservation_uuid: UUID
    reservation_creation_date: datetime


class DeleteReservation(BaseModel):
    reservation_uuid: UUID


class updateReservationResponse(BaseModel):
    reservation_uuid: UUID
    reservation_creation_date: datetime
    item_id: UUID
    item_name: str
    item_qty: int
    foodbank_id: UUID


class GetReservationResponse(BaseModel):
    reservation_uuid: UUID
    reservation_creation_date: datetime
    foodbank_id: UUID
    user_uuid: UUID
    showed_up_time: datetime
    showed_up: bool
    current_status: str
    reservations_array: List[ReservationItem]


class ReservationItemUpdate(BaseModel):
    item_id: Optional[UUID]
    item_name: Optional[str]
    item_qty: Optional[int]
    current_status: Optional[str]


class ReservationUpdate(BaseModel):
    reserve_time: Optional[datetime]
    user_uuid: Optional[UUID]
    showed_up_time: Optional[datetime]
    showed_up: Optional[bool]
    reservations_array: Optional[List[ReservationItemUpdate]]
    current_status: Optional[str]
