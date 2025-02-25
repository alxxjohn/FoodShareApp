from typing import Optional
from dataclasses import asdict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

# from fastapi.security import OAuth2PasswordBearer


from foodshareapp.db.utils import Transaction, db_transaction
from foodshareapp.app.api.models.user import ReturnUserResponse, DeleteUser
import foodshareapp.db.models.user as db_user

# TODO add token and auth
# reuseable_oauth = OAuth2PasswordBearer(
#     tokenUrl="/api/auth/login",
#     scheme_name="JWT"
# )

router = APIRouter(dependencies=[Depends(db_transaction)])


@router.get(
    "/{uuid}/", status_code=status.HTTP_200_OK, response_model=ReturnUserResponse
)
async def get_user_id(
    uuid: UUID, transaction: Transaction = Depends(db_transaction)
) -> Optional[ReturnUserResponse]:
    """Returns user by `uuid`"""

    return_user = await db_user.get_user_by_id(uuid)
    if return_user is None:
        raise HTTPException(
            status_code=404,
            detail="this user doesnt exist",
        )

    print(return_user)

    response = ReturnUserResponse(**asdict(return_user))

    await transaction.commit()
    return response


@router.get("/", status_code=status.HTTP_200_OK, response_model=ReturnUserResponse)
async def get_user_email(
    email: str, transaction: Transaction = Depends(db_transaction)
) -> Optional[ReturnUserResponse]:
    """Returns user by `email`"""

    return_user = await db_user.get_user_by_email(email)
    if return_user is None:
        raise HTTPException(
            status_code=404,
            detail="this user doesnt exist",
        )
    print(return_user)

    response = ReturnUserResponse(**asdict(return_user))

    await transaction.commit()
    return response


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    delete_user: DeleteUser, transaction: Transaction = Depends(db_transaction)
):
    """Deletes the user given by `user_email`"""

    await db_user.delete_user_by_email(delete_user.email)
    await transaction.commit()
