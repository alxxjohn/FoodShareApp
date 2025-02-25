from pydantic import BaseModel, validator, EmailStr
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID


class NewUser(BaseModel):
    uuid: UUID
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    password: str
    salt: str
    last_login = datetime.now(timezone.utc)


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    password: str
    terms: bool

    _validate_password = validator("password", allow_reuse=True)


class CreateUserResponse(BaseModel):
    uuid: UUID
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    password: Optional[str]
