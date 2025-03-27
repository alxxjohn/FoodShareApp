from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserBusiness(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    username: str
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
    BusinessId: UUID
    companyName: str
    isFoodbank: bool
    assoc_user: UUID
    is_business: bool = False
    is_admin: bool = False


class NewBusiness(BaseModel):
    """""
    DTO for business models."
    """ ""

    BusinessId: UUID
    companyName: str
    address: str
    city: str
    state: str
    zipCode: str
    lat: str
    lng: str
    isFoodbank: bool
    assoc_user: UUID


class CreateBusinessResponse(BaseModel):
    """""
    DTO for business models."
    """ ""

    BusinessId: UUID
    companyName: str
    address: str
    city: str
    state: str
    zipCode: str
    lat: str
    lng: str
    isFoodbank: bool
    assoc_user: UUID


class CreateUserBusiness:

    firstname: str
    lastname: str
    password: str
    email: EmailStr
    username: str
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
    is_business: bool = False
    is_admin: bool = False

    class Config:
        orm_mode = True
