from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from foodshareapp.app.api.services.crypto import JWT_ALGORITHM, JWT_SECRET_KEY

from jose import jwt
from pydantic import ValidationError
from foodshareapp.app.api.models.auth import TokenPayload
import foodshareapp.db.models.auth as db_user

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")


async def get_current_user(token: str = Depends(reuseable_oauth)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**dict(payload))
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(token_data.sub)
    user = await db_user.get_token_data(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return {"uuid": user.uuid, "email": user.email, "username": user.username}
