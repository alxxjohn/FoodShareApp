from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from foodshareapp.db.utils import Transaction, db_transaction
from foodshareapp.app.api.models.reservations import CreateReservation, CreateReservationResponse, updateReservationResponse, Reservation
import foodshareapp.db.models.user as db_user

timestamp = datetime.now(timezone.utc)
router = APIRouter(dependencies=[Depends(db_transaction)])
curr_userId = "12345678-1234-5678-1234-567812345678"  # Placeholder for userId


@router.post(
    "/", status_code=status.HTTP_200_OK, response_model=CreateReservationResponse
)
async def create_reservation(
    create_reservation: CreateReservation, transaction: Transaction = Depends(db_transaction)
) -> CreateReservationResponse:
    """ Creates reservation."""

    if await db_user.get_reservation_by_id(create_reservation.reservationID) is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="a reservation with that ID already exists",
        )

    new_reservation = CreateReservation(
        reservationID=uuid4(),
        reservationMadeTime=timestamp,
        foodbankId=create_reservation.foodbankId,
        itemId=create_reservation.itemId,
        itemName=create_reservation.itemName,
        userId=curr_userId,
        itemQty=create_reservation.itemQty,
        status=create_reservation.status,
    )
    await db_user.insert_reservation(new_reservation)
    await transaction.commit()

    response = CreateReservationResponse(
        reservationID=new_reservation.reservationID,
        reservationMadeTime=new_reservation.reservationMadeTime,
    )
    return response


@router.patch(
    "/{reservationID}/", status_code=status.HTTP_200_OK, response_model=updateReservationResponse
)
async def update_reservation(
    reservationID: UUID, transaction: Transaction = Depends(db_transaction)
) -> CreateReservationResponse:
    """ Updates reservation by `reservationID`."""

    reservation = await db_user.get_reservation_by_id(reservationID)
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this reservation does not exist",
        )

    updated_reservation = CreateReservationResponse(
        reservationID=reservation.reservationID,
        reservationMadeTime=reservation.reservationMadeTime,
        foodbankId=reservation.foodbankId,
        itenName=reservation.itenName,
        itemId=reservation.itemId,
        userId=reservation.userId,
        itemQty=reservation.itemQty,
        status=reservation.status,
    )
    await db_user.update_reservation(updated_reservation)
    await transaction.commit()

    return updated_reservation


@router.get(
    "/{reservationID}/", status_code=status.HTTP_200_OK, response_model=Reservation
)
async def get_reservation(
    reservationID: UUID, transaction: Transaction = Depends(db_transaction)
) -> Reservation:
    """ Gets reservation by `reservationID`."""

    reservation = await db_user.get_reservation_by_id(reservationID)
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this reservation does not exist",
        )

    response = Reservation(**reservation)
    return response


@router.delete(
    "/{reservationID}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_reservation(
    reservationID: UUID, transaction: Transaction = Depends(db_transaction)
):
    """ Deletes reservation given by `reservationID`"""

    await db_user.delete_reservation(reservationID)
    await transaction.commit() 
    return reservationID