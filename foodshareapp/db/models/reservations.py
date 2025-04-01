from dataclasses import asdict
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
import json
from pydantic import BaseModel


from foodshareapp.db.utils import db
from foodshareapp.db.models.inventory import db as inventory_db
from foodshareapp.app.api.models.reservations import CreateReservationItem


class ReservationItem(BaseModel):
    item_id: UUID
    item_name: str
    item_qty: int
    current_status: str


class Reservation(BaseModel):
    reservation_uuid: UUID
    reserve_time: datetime
    reservation_creation_date: datetime
    user_uuid: UUID
    showed_up_time: Optional[datetime]
    showed_up: bool
    reservations_array: List[ReservationItem]
    current_status: str = "active"


class CreateReservation(BaseModel):
    reserve_time: datetime
    reservations_array: List[CreateReservationItem]


class CreateReservationResponse(Reservation):
    reservation_uuid: UUID
    reservation_creation_date: datetime


async def get_inventory_item_by_id(item_id: UUID):
    query = "SELECT * FROM inventory WHERE item_id = :item_id"
    return await db.fetch_one(query, {"item_id": item_id})


async def update_inventory_quantity(item_id: UUID, quantity: int):
    stmt = """
        UPDATE inventory
        SET item_qty = :quantity,
            item_status = CASE WHEN :quantity = 0 THEN 'reserved' ELSE item_status END
        WHERE item_id = :item_id
    """
    await db.execute(stmt, {"item_id": item_id, "quantity": quantity})


async def get_reservation_by_id(reservation_uuid: UUID) -> Optional[Reservation]:
    stmt = "SELECT * FROM reservations WHERE reservation_uuid = :reservation_uuid"
    db_reservation = await db.fetch_one(
        stmt, values={"reservation_uuid": reservation_uuid}
    )

    if db_reservation is None:
        return None

    return Reservation(**dict(db_reservation))


async def insert_reservation(
    reservation: CreateReservation, user_uuid: UUID
) -> CreateReservationResponse:
    reservation_uuid = uuid4()
    creation_date = datetime.utcnow()
    updated_reservations_array = []

    for item in reservation.reservations_array:
        inventory_query = """
            SELECT item_name, item_qty
            FROM inventory
            WHERE item_id = :item_id
        """
        inventory_record = await db.fetch_one(
            inventory_query, {"item_id": str(item.item_id)}
        )

        if not inventory_record:
            raise ValueError(f"Inventory item {item.item_id} not found")

        new_qty = inventory_record["item_qty"] - item.item_qty
        if new_qty < 0:
            raise ValueError(
                f"Requested quantity exceeds available stock for {inventory_record['item_name']}"
            )

        item_status = "reserved" if new_qty == 0 else "available"

        update_inventory_query = """
            UPDATE inventory
            SET item_qty = :new_qty,
                item_status = :item_status
            WHERE item_id = :item_id
        """
        await db.execute(
            update_inventory_query,
            {
                "new_qty": new_qty,
                "item_status": item_status,
                "item_id": str(item.item_id),
            },
        )

        updated_reservations_array.append(
            {
                "item_id": str(item.item_id),
                "item_name": inventory_record["item_name"],
                "item_qty": item.item_qty,
                "current_status": item_status,
            }
        )

    insert_reservation_query = """
        INSERT INTO reservations (
            reservation_uuid,
            reservation_creation_date,
            reserve_time,
            user_uuid,
            picked_up,
            picked_up_time,
            reservations_array,
            current_status
        )
        VALUES (
            :reservation_uuid,
            :reservation_creation_date,
            :reserve_time,
            :user_uuid,
            :picked_up,
            :picked_up_time,
            :reservations_array,
            :current_status
        )
    """

    await db.execute(
        insert_reservation_query,
        {
            "reservation_uuid": str(reservation_uuid),
            "reservation_creation_date": creation_date,
            "reserve_time": reservation.reserve_time,
            "user_uuid": str(user_uuid),
            "picked_up": False,
            "picked_up_time": None,
            "reservations_array": [
                json.dumps(item, default=str) for item in updated_reservations_array
            ],
            "current_status": "reserved",
        },
    )

    return CreateReservationResponse(
        reservation_uuid=reservation_uuid,
        reservation_creation_date=creation_date,
        reserve_time=reservation.reserve_time,
        item_id=item.item_id,
        item_name=inventory_record["item_name"],
        user_uuid=user_uuid,
        item_qty=item.item_qty,
        showed_up=False,
        showedUpTime=None,
        current_status="reserved",
        reservations_array=updated_reservations_array,
    )


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
