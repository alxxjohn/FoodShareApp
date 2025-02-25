from uuid import uuid4
from datetime import datetime
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from foodshareapp.db.utils import Transaction, db_transaction
from foodshareapp.db.models.user import NewUser
from foodshareapp.app.api.models.register import CreateUser, CreateUserResponse
from foodshareapp.app.api.services.crypto import gen_salt, hash_password
import foodshareapp.db.models.user as db_user


# reuseable_oauth = OAuth2PasswordBearer(
#     tokenUrl="/api/auth/login",
#     scheme_name="JWT"
# )

router = APIRouter(dependencies=[Depends(db_transaction)])


# TODO add last login
@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def register(
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
    )
    await db_user.insert_user(new_user)

    response = CreateUserResponse(
        uuid=new_user.uuid,
        email=EmailStr(new_user.email),
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        password=new_user.password,
    )
    await transaction.commit()
    return response
