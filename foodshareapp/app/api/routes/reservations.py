from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from foodshareapp.db.utils import Transaction, db_transaction
from foodshareapp.app.api.services.auth import get_current_user
from foodshareapp.app.api.models.reservations import (
    CreateReservationResponse,
    CreateReservation,
)
from foodshareapp.db.models import reservations as db_reservations


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")


timestamp = datetime.now(timezone.utc)
router = APIRouter(dependencies=[Depends(db_transaction), Depends(get_current_user)])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CreateReservationResponse,
)
async def create_reservation(
    create_reservation: CreateReservation,
    transaction: Transaction = Depends(db_transaction),
    current_user: dict = Depends(get_current_user),
) -> CreateReservationResponse:
    """Creates reservation and updates inventory."""

    current_user_id = current_user["uuid"]

    new_reservation = db_reservations.Reservation(
        reservationID=uuid4(),
        reservation_creation_date=timestamp,
        foodbank_id=create_reservation.foodbank_id,
        item_id=create_reservation.item_id,
        item_name=create_reservation.item_name,
        current_user_id=current_user_id,
        picked_up=create_reservation.picked_up,
        showedUp=False,
        current_status="reserved",
    )

    await db_reservations.insert_reservation(new_reservation)

    inventory_item = await db_reservations.get_inventory_item_by_id(
        create_reservation.itemId
    )
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    new_quantity = inventory_item.quantity - create_reservation.itemQty
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Not enough inventory")

    inventory_item.quantity = new_quantity

    if new_quantity == 0:
        inventory_item.status = "reserved"

    await db_reservations.update_inventory_item(inventory_item)

    await transaction.commit()

    response = CreateReservationResponse(
        reservation_uuid=new_reservation.reservation_uuid,
        reservation_creation_date=new_reservation.reservation_creation_date,
        item_id=create_reservation.item_id,
        item_name=create_reservation.itemName,
        item_qty=create_reservation.item_qty,
        foodbank_id=create_reservation.foodbank_id,
    )
    return response


@router.patch(
    "/{reservationID}/",
    status_code=status.HTTP_200_OK,
    response_model=db_reservations.Reservation,
)
async def update_reservation(
    reservationID: UUID, transaction: Transaction = Depends(db_transaction)
) -> db_reservations.Reservation:
    """Updates reservation by `reservationID`."""

    reservation = await db_reservations.get_reservation_by_id(reservationID)
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this reservation does not exist",
        )

    updated_reservation = db_reservations.Reservation(
        reservationID=reservation.reservationID,
        reservationMadeTime=reservation.reservationMadeTime,
        foodbankId=reservation.foodbankId,
        itenName=reservation.itenName,
        itemId=reservation.itemId,
        userId=reservation.userId,
        itemQty=reservation.itemQty,
        status=reservation.status,
    )
    await db_reservations.update_reservation(updated_reservation)
    await transaction.commit()

    return updated_reservation


@router.get(
    "/{reservationID}/",
    status_code=status.HTTP_200_OK,
    response_model=db_reservations.Reservation,
)
async def get_reservation(
    reservationID: UUID, transaction: Transaction = Depends(db_transaction)
) -> db_reservations.Reservation:
    """Gets reservation by `reservationID`."""

    reservation = await db_reservations.get_reservation_by_id(reservationID)
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this reservation does not exist",
        )

    return reservation


@router.delete("/{reservationID}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservationID: UUID, transaction: Transaction = Depends(db_transaction)
) -> UUID:
    """Deletes reservation given by `reservationID`"""

    await db_reservations.delete_reservation(reservationID)
    await transaction.commit()
    return reservationID
