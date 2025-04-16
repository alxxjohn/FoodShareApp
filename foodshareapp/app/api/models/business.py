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
    zipcode: str
    lat: str
    lng: str
    phone: str
    business_id: UUID
    company_name: str
    is_foodbank: bool
    assoc_user: UUID
    is_business: bool = False
    is_admin: bool = False


class NewBusiness(BaseModel):
    """""
    DTO for business models."
    """ ""

    business_id: UUID
    company_name: str
    address: str
    city: str
    state: str
    zipcode: str
    lat: str
    lng: str
    isFoodbank: bool
    assoc_user: UUID


class CreateBusinessResponse(BaseModel):
    """""
    DTO for business models."
    """ ""

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
