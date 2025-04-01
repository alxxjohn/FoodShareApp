from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID, uuid4
import json
from pydantic import BaseModel


from foodshareapp.db.utils import db
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
    picked_up_time: Optional[datetime]
    picked_up: bool
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

    raw = dict(db_reservation)
    raw.setdefault("showed_up", False)
    raw_array = raw.get("reservations_array")
    if isinstance(raw_array, list):
        parsed_array = []
        for item in raw_array:
            if isinstance(item, str):
                parsed_array.append(json.loads(item))  # Parse JSON string to dict
            elif isinstance(item, dict):
                parsed_array.append(item)
        raw["reservations_array"] = parsed_array
    else:
        raw["reservations_array"] = []
    return Reservation(**raw)


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

        inv_qty = int(inventory_record["item_qty"])
        req_qty = int(item.item_qty)
        new_qty = inv_qty - req_qty
        print(
            f"[DEBUG] item: {inventory_record['item_name']}, inventory: {inv_qty}, requested: {req_qty}, new: {new_qty}"
        )

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
        user_uuid=user_uuid,
        showed_up=False,
        showedUpTime=None,
        picked_up=False,
        current_status="reserved",
        reservations_array=updated_reservations_array,
    )


async def delete_reservation(reservation_uuid: UUID) -> UUID:
    stmt = "DELETE FROM reservations WHERE reservation_uuid = :reservation_uuid"
    await db.execute(stmt, values={"reservation_uuid": reservation_uuid})
    return reservation_uuid


async def cleanup_expired_reservations() -> list[dict]:
    expiration_threshold = datetime.utcnow() - timedelta(hours=1)

    query = """
        SELECT reservation_uuid, reservations_array
        FROM reservations
        WHERE picked_up = FALSE AND reserve_time < :threshold AND current_status = 'reserved'
    """
    expired_reservations = await db.fetch_all(
        query, {"threshold": expiration_threshold}
    )

    restored_items = []

    for reservation in expired_reservations:
        reservation_uuid = reservation["reservation_uuid"]
        reservations_array = reservation["reservations_array"]

        try:
            items = json.loads(reservations_array)
        except Exception as e:
            print(
                f"[ERROR] Could not parse reservations_array for {reservation_uuid}: {e}"
            )
            continue

        for item in items:
            item_id = UUID(item["item_id"])
            item_qty = item["item_qty"]

            await db.execute(
                """
                UPDATE inventory
                SET item_qty = item_qty + :qty,
                    item_status = 'available'
                WHERE item_id = :item_id
            """,
                {"qty": item_qty, "item_id": str(item_id)},
            )

            restored_items.append(
                {
                    "reservation_uuid": str(reservation_uuid),
                    "item_id": str(item_id),
                    "item_name": item.get("item_name", "unknown"),
                    "restored_qty": item_qty,
                }
            )

        await db.execute(
            """
            UPDATE reservations
            SET current_status = 'expired'
            WHERE reservation_uuid = :uuid
        """,
            {"uuid": str(reservation_uuid)},
        )

    return restored_items


async def update_reservation_partial(reservation_uuid: UUID, updates: dict):
    if not updates:
        raise ValueError("No fields provided for update.")

    set_clause = ", ".join(f"{key} = :{key}" for key in updates)
    updates["reservation_uuid"] = str(reservation_uuid)

    query = f"""
        UPDATE reservations
        SET {set_clause}
        WHERE reservation_uuid = :reservation_uuid
    """
    await db.execute(query, updates)


async def delete_inventory_for_reservation(reservation: Reservation):
    for item in reservation.reservations_array:
        await db.execute(
            "DELETE FROM inventory WHERE item_id = :item_id",
            {"item_id": item.item_id}
        )
