from uuid import uuid4
from datetime import datetime
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status


from foodshareapp.db.utils import Transaction, db_transaction
from foodshareapp.db.models.user import NewUser
from foodshareapp.db.models.business import NewBusiness, CreateUserBusiness
from foodshareapp.app.api.models.register import CreateUser, CreateUserResponse
from foodshareapp.app.api.models.business import CreateBusinessResponse
from foodshareapp.app.api.services.crypto import gen_salt, hash_password
import foodshareapp.db.models.user as db_user
import foodshareapp.db.models.business as db_business
from foodshareapp.app.api.services.geocode import geocode_address

router = APIRouter(dependencies=[Depends(db_transaction)])


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
        uuid=uuid4(),
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
        zipcode=create_user.zipcode,
        phone=create_user.phone,
        is_business=create_user.is_business is True,
        is_admin=create_user.is_admin is True,
    )
    await db_user.insert_user(new_user)

    response = CreateUserResponse(
        uuid=new_user.uuid,
        email=EmailStr(new_user.email),
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        password=new_user.password,
        address=new_user.address is None,
        city=new_user.city is None,
        state=new_user.state is None,
        zipcode=new_user.zipcode is None,
        phone=new_user.phone is None,
        is_business=new_user.is_business is True,
        is_admin=new_user.is_admin is True,
    )
    await transaction.commit()
    return response


@router.post("/business", response_model=CreateBusinessResponse)
async def register_business(user_data: CreateUserBusiness) -> CreateBusinessResponse:
    """
    Creates a business model in the database.
    This also create a login user for the business Account.
    """

    salt = gen_salt()
    password = hash_password(user_data.password, salt)
    uuid = uuid4()
    full_address = (
        f"{user_data.address}, {user_data.city}, {user_data.state} {user_data.zipcode}"
    )
    lat, lng = geocode_address(full_address)

    new_user = NewUser(
        uuid=uuid,
        email=user_data.email,
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        password=password,
        salt=salt,
        address=user_data.address,
        city=user_data.city,
        state=user_data.state,
        zipcode=user_data.zipcode,
        phone=user_data.phone,
        is_business=user_data.is_business,
        is_admin=user_data.is_admin,
        last_login=datetime.utcnow(),
    )

    try:
        await db_user.insert_user(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User insertion failed: {e}")

    if user_data.is_business:
        new_business = NewBusiness(
            business_id=uuid4(),
            company_name=user_data.company_name,
            address=user_data.address,
            city=user_data.city,
            state=user_data.state,
            zipcode=user_data.zipcode,
            lat=str(lat) if lat else "",
            lng=str(lng) if lng else "",
            is_foodbank=user_data.is_foodbank,
            assoc_user=uuid,
        )
        try:
            await db_business.insert_business(new_business)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Business insertion failed: {e}"
            )

    return CreateBusinessResponse(
        business_id=new_business.business_id,
        company_name=new_business.company_name,
        address=new_business.address,
        city=new_business.city,
        state=new_business.state,
        zipcode=new_business.zipcode,
        lat=new_business.lat,
        lng=new_business.lng,
        is_foodbank=new_business.is_foodbank,
        assoc_user=new_business.assoc_user,
    )
