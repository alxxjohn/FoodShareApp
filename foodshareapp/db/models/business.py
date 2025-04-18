from dataclasses import dataclass
from pydantic import EmailStr
from datetime import datetime
from dataclasses import asdict
from typing import Optional
from uuid import UUID


from foodshareapp.db.utils import db


@dataclass
class CreateBusiness:

    firstname: str
    lastname: str
    password: str
    tos_accepted: Optional[bool]
    tos_accepted_date: Optional[datetime]
    last_login: Optional[datetime]
    bad_login_attempt: Optional[datetime]
    bad_login_count: Optional[int]
    account_locked: bool
    account_verified: bool
    account_verified_at: Optional[datetime]
    address: str
    city: str
    state: str
    zipcode: str
    lat: str
    lng: str
    phone: str
    companyName: str
    is_foodbank: bool = False
    is_business: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True


@dataclass
class BusinessModel:
    business_id: UUID
    company_name: str
    address: str
    city: str
    state: str
    zipcode: str
    lat: str
    lng: str
    is_foodbank: bool
    assoc_user: UUID


@dataclass
class NewBusiness:
    __tablename__ = "businesses"
    business_id: UUID
    company_name: str
    address: str
    city: str
    state: str
    zipcode: str
    lat: str
    lng: str
    is_foodbank: bool
    assoc_user: UUID


@dataclass
class CreateUserBusiness:
    firstname: str
    lastname: str
    password: str
    company_name: str
    email: EmailStr
    username: str
    tos_accepted: Optional[bool]
    address: str
    city: str
    state: str
    zipcode: str
    phone: str
    is_business: bool = True
    is_foodbank: bool = False
    is_admin: bool = False


async def insert_business(NewBusiness: NewBusiness) -> UUID:
    """Creates a new business"""

    stmnt = (
        "INSERT INTO business (business_id, company_name, address, city, state, zipcode, lat, lng, is_foodbank, assoc_user) "
        "VALUES (:business_id, :company_name, :address, :city, :state, :zipcode, :lat, :lng, :is_foodbank, :assoc_user)"
    )
    return await db.execute(stmnt, values=asdict(NewBusiness))


async def get_business_by_business_id(business_id: UUID) -> Optional[BusinessModel]:
    """Returns the business with the given id.
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT * FROM business WHERE business_id = :business_id"
    db_user = await db.fetch_one(query=stmnt, values={"business_id": business_id})

    if db_user is None:
        return None

    return BusinessModel(**dict(db_user))
