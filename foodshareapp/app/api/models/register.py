from pydantic import BaseModel, validator, EmailStr
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID


class NewUser(BaseModel):
    uuid: UUID
    email: EmailStr
    company_name: Optional[str]
    username: str
    firstname: str
    lastname: str
    password: str
    salt: str
    last_login = datetime.now(timezone.utc)
    company_name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    phone: Optional[str]
    is_business: bool = False
    is_admin: bool = False


class CreateUser(BaseModel):
    email: EmailStr
    company_name: Optional[str]
    username: str
    firstname: Optional[str]
    lastname: Optional[str]
    password: str
    terms: bool
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    phone: Optional[str]
    is_business: bool
    is_admin: bool

    _validate_password = validator("password", allow_reuse=True)


class CreateUserResponse(BaseModel):
    uuid: UUID
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    password: Optional[str]
