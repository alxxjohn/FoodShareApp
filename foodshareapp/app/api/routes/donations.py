from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from foodshareapp.db.utils import Transaction, db_transaction
from fastapi.security import OAuth2PasswordBearer


from foodshareapp.db.models.donations import Donation, DonationItemResponse
from foodshareapp.app.api.models.donations import CreateDonation, CreateDonationResponse
from foodshareapp.app.api.services.auth import get_current_user


import foodshareapp.db.models.donations as db_donation


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")
router = APIRouter(dependencies=[Depends(db_transaction), Depends(get_current_user)])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateDonationResponse
)
async def create_donation(
    create_donation: CreateDonation,
    transaction: Transaction = Depends(db_transaction),
    current_user: dict = Depends(get_current_user),
):
    current_user_id = current_user["uuid"]

    foodbank_id = await db_donation.get_foodbank_id_for_user(current_user_id)
    if foodbank_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foodbank not found for user",
        )

    donation_id = uuid4()
    timestamp = datetime.now(timezone.utc)

    donation_items = []
    for item in create_donation.donations_array:
        item_id = uuid4()
        donation_items.append(
            DonationItemResponse(
                item_id=item_id, item_name=item.item_name, item_qty=item.item_qty
            )
        )

        await db_donation.upsert_inventory_item(
            foodbank_id=foodbank_id,
            item_id=item_id,
            item_name=item.item_name,
            item_qty=item.item_qty,
        )

    donation = Donation(
        donation_id=donation_id,
        donation_creation_date=timestamp,
        foodbank_id=foodbank_id,
        donations_array=donation_items,
        status="available",
    )

    return await db_donation.insert_donation(donation)


@router.get("/{donation_id}", status_code=status.HTTP_200_OK, response_model=Donation)
async def get_donation(donation_id: UUID) -> Donation:
    """
    get a donation by `donation_id`.

    """

    donation = await db_donation.get_donation_by_id(donation_id)
    if donation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )
    return Donation(**donation.dict())


@router.delete("/{donation_id}", status_code=status.HTTP_200_OK)
async def delete_donation(donation_id: UUID) -> datetime:
    """
    Delete a donation by `donationID`.
    """
    donation = await db_donation.get_donation_by_id(donation_id)
    if donation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )
    await db_donation.delete_donation(donation_id)
    deleteTimestamp = datetime.now(timezone.utc)
    return deleteTimestamp
