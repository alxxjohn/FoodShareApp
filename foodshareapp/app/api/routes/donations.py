from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from foodshareapp.db.utils import Transaction, db_transaction
from foodshareapp.app.api.models.donations import GetDonationsResponse, GetDonationResponse, CreateDonationResponse, Donations


router = APIRouter(dependencies=[Depends(db_transaction)])


@router.get("/donations"
            , response_model=GetDonationsResponse)
async def get_donations() -> None:
    """
    Get all donations.
    """
    pass


@router.get("/donations/{donation_id}"
            , response_model=GetDonationResponse)
async def get_donation(
    get_donation: Donations, transaction: Transaction = Depends(db_transaction)
) -> GetDonationResponse:
    """
    Get a donation by ID.
    """
    pass


@router.post("/donations"
             , status_code=status.HTTP_201_CREATED
             , response_model=CreateDonationResponse)
async def create_donation() -> None:
    """
    Create a new donation.
    """
    pass