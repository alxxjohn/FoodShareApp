from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    uuid: UUID
    email: EmailStr
    username: str


class User(UserBase):
    """
    DTO for user models.

    returned when accessing user models from the API.
    """

    firstname: str
    lastname: str
    password: Optional[str]
    tos_accepted: Optional[bool]
    tos_accepted_date: Optional[datetime]
    last_login: Optional[datetime]
    bad_login_attempt: Optional[datetime]
    bad_login_count: Optional[int]
    account_locked: bool
    account_verified: bool
    account_verified_at: Optional[datetime]

    class Config:
        orm_mode = True


class ReturnUserResponse(User):
    pass


class DeleteUser(BaseModel):
    email: EmailStr
