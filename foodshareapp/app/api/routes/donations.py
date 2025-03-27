from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from foodshareapp.db.utils import Transaction, db_transaction
from fastapi.security import OAuth2PasswordBearer


# from foodshareapp.db.models.donations import Donation
from foodshareapp.app.api.models.donations import CreateDonation, CreateDonationResponse, Donation
from foodshareapp.app.api.services.auth import get_current_user


import foodshareapp.db.models.donations as db_donation


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")
router = APIRouter(dependencies=[Depends(db_transaction), Depends(get_current_user)])
current_user = get_current_user()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateDonationResponse
)
async def create_donation(
    create_donation: CreateDonation, transaction: Transaction = Depends(db_transaction)
) -> CreateDonationResponse:
    """
    Creates donation model in the database.

    """

    current_user_id = current_user["userId"]

    new_donation = Donation(
        donationID=uuid4(),
        donationMadeTime=datetime.now(timezone.utc),
        foodbankId=uuid4(),
        itemId=uuid4(),
        itemName=create_donation.itemName,
        userId=current_user_id,
        itemQty=create_donation.itemQty,
        pickupTime=None,
        status="Available",
    )
    await db_donation.insert_donation(new_donation)
    return CreateDonationResponse(**new_donation.dict())


# @router.get(
#     "/{donationID}", status_code=status.HTTP_200_OK, response_model=Donation)
# async def get_donation(donationID: uuid4) -> Donation:
#     """
#     Retrieves donation model from the database.

#     """

#     donation = await db_donation.get_donation_by_id(donationID)
#     if donation is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Donation not found",
#         )
#     return Donation(**dict(donation))


@router.delete(
    "/{donationID}", status_code=status.HTTP_200_OK
)
async def delete_donation(donationID: UUID) -> UUID:
    """
    Deletes donation model from the database.

    """

    donation = await db_donation.get_donation_by_id(donationID)
    if donation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )
    await db_donation.delete_donation(donationID)
    return donationID
