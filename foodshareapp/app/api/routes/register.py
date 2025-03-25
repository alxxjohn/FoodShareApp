from uuid import uuid4
from datetime import datetime, timezone
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from foodshareapp.db.utils import Transaction, db_transaction


from foodshareapp.db.models.user import NewUser
from foodshareapp.db.models.business import NewBusiness
from foodshareapp.app.api.models.register import CreateUser, CreateUserResponse
from foodshareapp.app.api.models.business import (
    CreateBusinessResponse,
    UserBusiness,
)
from foodshareapp.app.api.services.crypto import gen_salt, hash_password
import foodshareapp.db.models.user as db_user
import foodshareapp.db.models.business as db_business


router = APIRouter(dependencies=[Depends(db_transaction)])


# TODO add last login
@router.post(
    "/user", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def register_user(
    create_user: CreateUser, transaction: Transaction = Depends(db_transaction)
) -> CreateUserResponse:
    """
    Creates user model in the database.

    """

    if await db_user.get_user_by_email(create_user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="a user with that email already exists",
        )

    salt = gen_salt()
    password = hash_password(create_user.password, salt)
    new_user = NewUser(
        userId=uuid4(),
        email=EmailStr(create_user.email),
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        salt=salt,
        password=password,
        last_login=datetime.utcnow(),
        address=create_user.address,
        city=create_user.city,
        state=create_user.state,
        zipCode=create_user.zipCode,
        phone=create_user.phone,
        is_business=create_user.is_business is True,
        is_admin=create_user.is_admin is True,
    )
    await db_user.insert_user(new_user)

    response = CreateUserResponse(
        userId=new_user.userId,
        email=EmailStr(new_user.email),
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        password=new_user.password,
        address=new_user.address is None,
        city=new_user.city is None,
        state=new_user.state is None,
        zipCode=new_user.zipCode is None,
        phone=new_user.phone is None,
        is_business=new_user.is_business is True,
        is_admin=new_user.is_admin is True,
    )
    await transaction.commit()
    return response


@router.post("/business", response_model=CreateBusinessResponse)
async def register_business(user_data: UserBusiness) -> CreateBusinessResponse:
    """
    Creates a business model in the database.
    This also create a login user for the business Account.
    """

    salt = gen_salt()
    password = hash_password(user_data.password, salt)
    user_uuid = uuid4()

    new_user = NewUser(
        userId=user_uuid,
        email=user_data.email,
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        password=password,
        salt=salt,
        address=user_data.address,
        city=user_data.city,
        state=user_data.state,
        zipCode=user_data.zipCode,
        phone=user_data.phone,
        is_business=user_data.is_business,
        is_admin=user_data.is_admin,
        last_login=datetime.now(timezone.utc),
    )

    try:
        await db_user.insert_user(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User insertion failed: {e}")

    if user_data.is_business:
        new_business = NewBusiness(
            BusinessId=uuid4(),
            companyName=user_data.companyName,
            address=user_data.address,
            city=user_data.city,
            state=user_data.state,
            zipCode=user_data.zipCode,
            isFoodbank=user_data.isFoodbank,
            assoc_user=user_uuid,
        )
        try:
            await db_business.insert_business(new_business)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Business insertion failed: {e}"
            )

    return CreateBusinessResponse(
        userId=user_uuid,
        username=user_data.username,
        email=user_data.email,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        companyName=user_data.companyName,
    )
