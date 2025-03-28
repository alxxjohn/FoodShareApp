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
    zipCode: str
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
    BusinessId: UUID
    companyName: str
    address: str
    city: str
    state: str
    zipCode: str
    lat: str
    lng: str
    is_foodbank: bool
    assoc_user: UUID


@dataclass
class NewBusiness:
    __tablename__ = "businesses"
    BusinessId: UUID
    companyName: str
    address: str
    city: str
    state: str
    zipCode: str
    lat: str
    lng: str
    is_foodbank: bool
    assoc_user: UUID


@dataclass
class CreateUserBusiness:
    firstname: str
    lastname: str
    password: str
    companyName: str
    email: EmailStr
    username: str
    tos_accepted: Optional[bool]
    address: str
    city: str
    state: str
    zipCode: str
    phone: str
    is_business: bool = True
    is_foodbank: bool = False
    is_admin: bool = False


async def insert_business(NewBusiness: NewBusiness) -> UUID:
    """Creates a new business"""

    stmnt = (
        "INSERT INTO businesses (BusinessId, companyName, address, city, state, zipCode, lat, lng, is_foodbank, assoc_user) "
        "VALUES (:BusinessId, :companyName, :address, :city, :state, :zipCode, :lat, :lng, :is_foodbank, :assoc_user"
    )
    return await db.execute(stmnt, values=asdict(NewBusiness))


async def get_business_by_business_id(BusinessId: UUID) -> Optional[BusinessModel]:
    """Returns the business with the given id.
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT * FROM businesses WHERE BusinessId = :BusinessId"
    db_user = await db.fetch_one(query=stmnt, values={"BusinessId": BusinessId})

    if db_user is None:
        return None

    return BusinessModel(**dict(db_user))
