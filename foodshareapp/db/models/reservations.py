from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from foodshareapp.db.utils import db
from foodshareapp.db.models.inventory import db as inventory_db


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
    status: str = "active"


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
    stmt = "SELECT * FROM reservations WHERE reservationID = :reservationID"
    db_reservation = await db.fetch_one(stmt, values={"reservationID": reservationID})

    if db_reservation is None:
        return None

    return Reservation(**dict(db_reservation))


async def insert_reservation(reservation: Reservation) -> CreateReservationResponse:
    # Check available inventory before reserving
    check_stmt = "SELECT itemQty FROM inventory WHERE foodbankId = :foodbankId AND itemId = :itemId"
    inventory_record = await inventory_db.fetch_one(
        check_stmt,
        values={"foodbankId": reservation.foodbankId, "itemId": reservation.itemId},
    )

    if inventory_record is None or inventory_record["itemQty"] < reservation.itemQty:
        raise ValueError("Not enough inventory available to fulfill this reservation.")

    stmt = (
        "INSERT INTO reservations (reservationID, reservationMadeTime, foodbankId, itemId, itemName, userId, itemQty, pickupTime, showedUp, showedUpTime, status) "
        "VALUES (:reservationID, :reservationMadeTime, :foodbankId, :itemId, :itenName, :userId, :itemQty, :pickupTime, :showedUp, :showedUpTime, :status) "
        "RETURNING reservationID, reservationMadeTime"
    )
    await db.execute(stmt, values=asdict(reservation))

    # Update inventory (subtract itemQty)
    update_stmt = (
        "UPDATE inventory SET itemQty = itemQty - :qty "
        "WHERE foodbankId = :foodbankId AND itemId = :itemId AND itemQty >= :qty"
    )
    await inventory_db.execute(
        update_stmt,
        values={
            "qty": reservation.itemQty,
            "foodbankId": reservation.foodbankId,
            "itemId": reservation.itemId,
        },
    )

    return CreateReservationResponse(
        reservationID=reservation.reservationID,
        reservationMadeTime=reservation.reservationMadeTime,
        foodbankId=reservation.foodbankId,
        itemId=reservation.itemId,
        itenName=reservation.itenName,
        userId=reservation.userId,
        itemQty=reservation.itemQty,
        pickupTime=reservation.pickupTime,
        showedUp=reservation.showedUp,
        showedUpTime=reservation.showedUpTime,
        status=reservation.status,
    )


async def update_reservation(reservation: Reservation) -> Reservation:
    stmt = (
        "UPDATE reservations SET reservationMadeTime = :reservationMadeTime, foodbankId = :foodbankId, itemId = :itemId, itenName=:itemName, userId = :userId, itemQty = :itemQty, pickupTime = :pickupTime, showedUp = :showedUp, showedUpTime = :showedUpTime, status = :status "
        "WHERE reservationID = :reservationID"
    )
    await db.execute(stmt, values=asdict(reservation))

    # If user picked up item, delete from inventory
    if reservation.showedUp:
        delete_stmt = (
            "DELETE FROM inventory WHERE foodbankId = :foodbankId AND itemId = :itemId"
        )
        await inventory_db.execute(
            delete_stmt,
            values={"foodbankId": reservation.foodbankId, "itemId": reservation.itemId},
        )

    return reservation


async def delete_reservation(reservationID: UUID) -> UUID:
    stmt = "DELETE FROM reservations WHERE reservationID = :reservationID"
    await db.execute(stmt, values={"reservationID": reservationID})
    return reservationID
