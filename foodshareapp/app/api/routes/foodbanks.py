from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from foodshareapp.db.utils import db_transaction
from foodshareapp.db.models import reservations as db_reservations


timestamp = datetime.now(timezone.utc)
router = APIRouter(dependencies=[Depends(db_transaction)])
curr_userId = uuid4()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[db_reservations.Reservation],
)
async def get_all_foodbanks():
    """Get all foodbanks."""

    if not await db_reservations.get_all_foodbanks():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No foodbanks found",
        )
    return await db_reservations.get_all_foodbanks()


@router.get(
    "/{foodbank_id}/inventory",
    status_code=status.HTTP_200_OK,
    response_model=list[db_reservations.Reservation],
)
async def get_foodbank_inventory(foodbank_id: UUID):
    """Get foodbank inventory."""

    if not await db_reservations.get_foodbank_inventory(foodbank_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No inventory found",
        )
    return await db_reservations.get_foodbank_inventory(foodbank_id)


@router.get(
    "/{foodbank_id}/donations",
    status_code=status.HTTP_200_OK,
    response_model=list[db_reservations.Reservation],
)
async def get_foodbank_donations(foodbank_id: UUID):
    """Get foodbank donations."""
    if not await db_reservations.get_foodbank_donations(foodbank_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No donations found",
        )
    return await db_reservations.get_foodbank_donations(foodbank_id)
