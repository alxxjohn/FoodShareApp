from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer

from foodshareapp.db.models.auth import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from foodshareapp.app.api.services.auth import get_current_user
from foodshareapp.app.api.models.auth import TokenSchema, SystemUser
from foodshareapp.db.utils import Transaction, db_transaction

import foodshareapp.db.models.auth as db_user

router = APIRouter(dependencies=[Depends(db_transaction)])
security = HTTPBearer()

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    transaction: Transaction = Depends(db_transaction),
):
    user = await db_user.get_user_pass(form_data.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't exsist")
    login_count = user["bad_login_count"]
    timestamp = datetime.utcnow()
    hashed_pass = user["password"]
    email = user["email"]
    salt = user["salt"]
    locked = user["account_locked"]
    if not verify_password(form_data.password, hashed_pass, salt):
        login_count += 1
        await db_user.update_bad_login(email, timestamp, login_count)
        await transaction.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    login_count = 0
    if locked is not False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account Locked",
        )

    if await db_user.update_login(email, timestamp, login_count) is not True:
        await transaction.commit()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="this user doesnt exist",
        )
    return {
        "access_token": create_access_token(user["uuid"]),
        "refresh_token": create_refresh_token(user["uuid"]),
    }


@router.get("/user", summary="Get details of currently logged in user")
async def get_my_login(user: SystemUser = Depends(get_current_user)):
    return user
