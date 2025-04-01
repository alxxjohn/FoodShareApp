from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import UUID
import json
from pydantic import BaseModel
from sqlalchemy import text

from foodshareapp.db.utils import db
from foodshareapp.db.models.inventory import db as inventory_db


# TODO: remove address
@dataclass
class Reservation(BaseModel):
    reservation_uuid: UUID
    reservation_creation_date: datetime
    foodbankId: UUID
    item_id: UUID
    item_name: str
    user_uuid: UUID
    item_qty: int
    showed_up_time: datetime
    showed_up: bool
    showedUpTime: Optional[datetime]
    current_status: str = "active"


@dataclass
class CreateReservation:
    item_id: UUID
    user_uuid: UUID
    item_qty: int
    current_status: str


@dataclass
class CreateReservationResponse(Reservation):
    reservation_uuid: UUID
    reservation_creation_date: datetime


async def get_inventory_item_by_id(item_id: UUID):
    query = "SELECT * FROM inventory WHERE item_id = :item_id"
    return await db.fetch_one(query, {"item_id": item_id})


async def update_inventory_item(item):
    query = """
        UPDATE inventory
        SET item_qty = :item_qty, current_status = :current_status
        WHERE item_id = :item_id
    """
    await db.execute(
        query,
        {"item_id": item.item_id, "item_qty": item.item_qty, "current_status": item.current_status},
    )


async def get_reservation_by_id(reservation_uuid: UUID) -> Optional[Reservation]:
    stmt = "SELECT * FROM reservations WHERE reservation_uuid = :reservation_uuid"
    db_reservation = await db.fetch_one(
        stmt, values={"reservation_uuid": reservation_uuid}
    )

    if db_reservation is None:
        return None

    return Reservation(**dict(db_reservation))


async def insert_reservation(reservation: CreateReservation) -> CreateReservationResponse:
    async with db.transaction():

        insert_stmt = """
            INSERT INTO reservations (
                reservation_uuid, reservation_creation_date, user_uuid,
                picked_up, picked_up_time, reservations_array, current_status
            )
            VALUES (
                :reservation_uuid, :reservation_creation_date, :user_uuid,
                :picked_up, :picked_up_time, :reservations_array, :current_status
            )
        """

        await db.execute(
            insert_stmt,
            values={
                "reservation_uuid": reservation.reservation_uuid,
                "reservation_creation_date": reservation.reservation_creation_date,
                "user_uuid": reservation.user_uuid,
                "picked_up": reservation.picked_up,
                "picked_up_time": reservation.picked_up_time,
                "reservations_array": [json.dumps(item.dict(), default=str) for item in reservation.reservations_array],
                "current_status": reservation.current_status,
            }
        )

        # Step 2: Update inventory per item
        for item in reservation.reservations_array:
            update_stmt = text("""
                UPDATE foodbankinventory
                SET quantity = quantity - :reserved_quantity,
                    status = CASE
                        WHEN quantity - :reserved_quantity <= 0 THEN 'reserved'
                        ELSE status
                    END
                WHERE inventory_id = :inventory_id
            """)
            await db.execute(
                update_stmt,
                values={
                    "inventory_id": str(item.inventory_id),
                    "reserved_quantity": item.quantity
                }
            )

    return CreateReservationResponse(**reservation.dict())


async def update_reservation(reservation: Reservation) -> Reservation:
    stmt = (
        "UPDATE reservations SET reservation_creation_date = :reservation_creation_date, foodbank_id = :foodbank_id, item_id = :item_id, item_name=:item_name, userId = :userId, itemQty = :itemQty, pickupTime = :pickupTime, showedUp = :showedUp, showedUpTime = :showedUpTime, status = :status "
        "WHERE reservation_uuid = :reservation_uuid"
    )
    await db.execute(stmt, values=asdict(reservation))

    # If user picked up item, delete from inventory
    if reservation.showedUp:
        delete_stmt = "DELETE FROM inventory WHERE foodbank_id = :foodbank_id AND itemId = :itemId"
        await inventory_db.execute(
            delete_stmt,
            values={
                "foodbank_id": reservation.foodbank_id,
                "itemId": reservation.itemId,
            },
        )

    return reservation


async def delete_reservation(reservation_uuid: UUID) -> UUID:
    stmt = "DELETE FROM reservations WHERE reservation_uuid = :reservation_uuid"
    await db.execute(stmt, values={"reservationID": reservation_uuid})
    return reservation_uuid
