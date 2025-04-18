from dataclasses import dataclass
from dataclasses import asdict
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from foodshareapp.db.utils import db


@dataclass
class UserModel:
    uuid: UUID
    email: str
    username: str
    firstname: str
    lastname: str
    salt: Optional[str]
    password: Optional[str]
    tos_accepted: bool
    tos_accepted_date: datetime
    last_login: Optional[datetime]
    bad_login_attempt: Optional[datetime]
    bad_login_count: Optional[int]
    account_locked: bool
    account_verified: bool
    account_verified_at: Optional[datetime]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    phone: Optional[str]
    is_business: bool
    is_admin: bool


@dataclass
class NewUser:
    __tablename__ = "users"
    uuid: UUID
    email: str
    username: str
    firstname: Optional[str]
    lastname: Optional[str]
    salt: str
    password: str
    last_login: datetime
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    phone: Optional[str]
    is_business: bool
    is_admin: bool


@dataclass
class PasswordResponse(BaseModel):
    password: str
    email: str


async def get_user_by_email(email: str) -> Optional[UserModel]:
    """Returns a single user row for the user matching the given email.
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT * FROM users WHERE email = :email"
    db_user = await db.fetch_one(query=stmnt, values={"email": email})

    if db_user is None:
        return None

    return UserModel(**dict(db_user))


async def insert_user(newuser: NewUser) -> UUID:
    """Creates a new user"""

    stmnt = (
        "INSERT INTO users (uuid, email, username, firstname, lastname, salt, password, last_login, address, city, state, zipcode, phone, is_business, is_admin) "
        "VALUES (:uuid, :email, :username, :firstname, :lastname, :salt, :password, :last_login, :address, :city, :state, :zipcode, :phone, :is_business, :is_admin) "
        "RETURNING uuid"
    )
    return await db.execute(stmnt, values=asdict(newuser))


async def get_user_by_id(uuid: UUID) -> Optional[UserModel]:
    """Returns the user with the given id.
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT * FROM users WHERE uuid = :uuid"
    db_user = await db.fetch_one(query=stmnt, values={"uuid": uuid})

    if db_user is None:
        return None

    return UserModel(**dict(db_user))


async def get_user_by_username(username: str) -> Optional[UserModel]:
    """Returns a single user row for the user matching the given email.
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT * FROM users WHERE username = :username"
    db_user = await db.fetch_one(query=stmnt, values={"username": username})

    if db_user is None:
        return None

    return UserModel(**dict(db_user))


async def delete_user_by_email(email: str) -> None:
    """Deletes the user with the given email"""

    stmnt = "DELETE FROM users WHERE email = :email"
    await db.execute(query=stmnt, values={"email": email})
