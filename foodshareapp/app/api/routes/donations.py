from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, Depends, status
from foodshareapp.db.utils import Transaction, db_transaction
from fastapi.security import OAuth2PasswordBearer


from foodshareapp.db.models.donations import Donation
from foodshareapp.app.api.models.donations import CreateDonation, CreateDonationResponse
from foodshareapp.app.api.services.auth import get_current_user


import foodshareapp.db.models.donations as db_donation


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")
router = APIRouter(dependencies=[Depends(db_transaction), Depends(get_current_user)])


@router.post(
    "/donations", status_code=status.HTTP_201_CREATED, response_model=CreateDonationResponse
)
async def create_donation(
    create_donation: CreateDonation, transaction: Transaction = Depends(db_transaction)
) -> CreateDonationResponse:
    """
    Creates donation model in the database.

    """

    new_donation = Donation(
        donationID=uuid4(),
        donationMadeTime=datetime.utcnow(),
        foodbankId=uuid4(),
        itemId=uuid4(),
        itemName=create_donation.itemName,
        userId=uuid4(),
        itemQty=create_donation.itemQty,
        pickupTime=create_donation.pickupTime,
        status=create_donation.status,
    )
    await db_donation.insert_donation(new_donation)
    return CreateDonationResponse(**new_donation.dict())
