from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from foodshareapp.app.api.services.auth import get_current_user
from foodshareapp.db.utils import Transaction, db_transaction
from foodshareapp.app.api.models.inventory import Inventory
from foodshareapp.db.models import inventory as db_inventory


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")


timestamp = datetime.now(timezone.utc)
router = APIRouter(dependencies=[Depends(db_transaction), Depends(get_current_user)])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[Inventory],
)
async def get_full_inventory(
    transaction: Transaction = Depends(db_transaction),
) -> List[Inventory]:
    """Get all inventories."""

    inventories = await db_inventory.list_inventory()
    if not inventories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No inventories found",
        )

    return [Inventory(**inv.dict()) for inv in inventories]
