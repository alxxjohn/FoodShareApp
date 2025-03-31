from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from foodshareapp.db.utils import db


@dataclass
class AuthResponse:
    uuid: UUID
    password: str
    salt: str
    email: str
    bad_login_count: int
    account_locked: bool

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class TokenResponse:
    token_sub: str
    token_exp: int

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class EmailResponse:
    email: str
    uuid: UUID
    password: str
    username: str


async def get_user_pass(username: str) -> Optional[AuthResponse]:
    """Returns a single user row for the user matching the given email.
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT uuid, password, email, salt, bad_login_count, account_locked FROM users WHERE username = :username"
    db_user = await db.fetch_one(query=stmnt, values={"username": username})

    if db_user is None:
        return None

    return AuthResponse(**dict(db_user))


async def update_login(
    email: str, last_login: datetime, bad_login_count: int
) -> Optional[AuthResponse]:
    """Updates a login date for user row"""
    stmnt = "UPDATE users SET last_login = :last_login, bad_login_count = :bad_login_count WHERE email = :email"
    await db.execute(
        stmnt,
        values={
            "email": email,
            "last_login": last_login,
            "bad_login_count": bad_login_count,
        },
    )
    return True


async def update_bad_login(
    email: str, bad_login_attempt: datetime, bad_login_count: int
) -> Optional[AuthResponse]:
    """Updates a login date for user row"""
    stmnt = "UPDATE users SET bad_login_attempt = :bad_login_attempt, bad_login_count = :bad_login_count WHERE email = :email"
    await db.execute(
        stmnt,
        values={
            "email": email,
            "bad_login_attempt": bad_login_attempt,
            "bad_login_count": bad_login_count,
        },
    )
    return True


async def get_user_by_email(email: str) -> Optional[EmailResponse]:
    """Returns a single user row for the user matching the given email.
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT * FROM users WHERE email = :email"
    db_user = await db.fetch_one(query=stmnt, values={"email": email})

    if db_user is None:
        return None

    return EmailResponse(**dict(db_user))


async def get_token_data(uuid: str) -> Optional[EmailResponse]:
    """Returns a single user token by userId
    Returns `None` if no such user exists.
    """

    stmnt = "SELECT uuid,email,password,username FROM users WHERE uuid = :uuid"
    db_user = await db.fetch_one(query=stmnt, values={"uuid": uuid})

    if db_user is None:
        return None

    return EmailResponse(**dict(db_user))
