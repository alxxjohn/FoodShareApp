from secrets import token_hex
import bcrypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "test"
JWT_SECRET = "test"  # should be kept secret
JWT_REFRESH_SECRET_KEY = "test"
TOKEN_NBYTES = 32

pwd_ctx = CryptContext(schemes=["bcrypt"])


def gen_salt() -> str:
    return bcrypt.gensalt(rounds=11).decode("utf-8")


def hash_password(password: str, salt: str = "") -> str:
    return pwd_ctx.hash(password + salt)


def verify_password(plain_password: str, hashed_password: str, salt: str = None):
    if salt is not None:
        plain_password += salt
    try:
        return pwd_ctx.verify(plain_password, hashed_password)
    except ValueError:
        return False


def random_secret_hex(nbytes: int = TOKEN_NBYTES):
    """Returns a cryptographically secure, hex-encoded token,
    with `nbytes` of randomness.
    """

    return token_hex(nbytes)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt