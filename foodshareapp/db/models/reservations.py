from dataclasses import dataclass
from dataclasses import asdict
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


from foodshareapp.db.utils import db


@dataclass
class Reservation(BaseModel):
    reservationID: UUID
    reservationMadeTime: datetime
    foodbankId: UUID
    itemId: UUID
    itenName: str
    userId: UUID
    itemQty: int
    pickupTime: datetime
    showedUp: bool
    showedUpTime: Optional[datetime]
    status: str = "active"  # default status is active


@dataclass
class CreateReservation:
    foodbankId: UUID
    itemId: UUID
    userId: UUID
    itemQty: int
    status: str


@dataclass
class CreateReservationResponse(Reservation):
    reservationID: UUID
    reservationMadeTime: datetime


async def get_reservation_by_id(reservationID: UUID) -> Optional[Reservation]:
    """Get reservation by ID."""

    stmt = "SELECT * FROM reservations WHERE reservationID = :reservationID"
    db_reservation = await db.fetch_one(stmt, values={"reservationID": reservationID})

    if db_reservation is None:
        return None

    return Reservation(**dict(db_reservation))


async def insert_reservation(reservation: Reservation) -> CreateReservationResponse:
    """Insert a new reservation."""

    stmt = (
        "INSERT INTO reservations (reservationID, reservationMadeTime, foodbankId, itemId, itemName, userId, itemQty, pickupTime, showedUp, showedUpTime, status "
        "VALUES (:reservationID, :reservationMadeTime, :foodbankId, :itemId, :itenName, :userId, :itemQty, :pickupTime, :showedUp, :showedUpTime, :status"
        "RETURNING reservationID,reservationMadeTime"
    )

    return await db.execute(stmt, values=asdict(reservation))


async def update_reservation(reservation: Reservation) -> Reservation:
    """Update an existing reservation."""

    stmnt = (
        "UPDATE reservations SET reservationMadeTime = :reservationMadeTime, foodbankId = :foodbankId, itemId = :itemId, itenName=:itemName, userId = :userId, itemQty = :itemQty, pickupTime = :pickupTime, showedUp = :showedUp, showedUpTime = :showedUpTime, status = :status "
        "WHERE reservationID = :reservationID"
    )
    await db.execute(stmnt, values=asdict(reservation))
    return reservation


async def delete_reservation(reservationID: UUID) -> UUID:
    """Delete a reservation."""

    stmnt = "DELETE FROM reservations WHERE reservationID = :reservationID"
    await db.execute(stmnt, values={"reservationID": reservationID})  # type: ignore
    return reservationID
