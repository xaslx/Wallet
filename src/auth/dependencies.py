from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_async_session
from exceptions import IncorrectTokenException, TokenAbsentException, UserIsNotPresentException
from src.models.user import User
from src.repositories.user import UserRepository




def get_token(request: Request):
    token: str = request.cookies.get("user_access_token")
    if not token:
        return None
    return token


def valid_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        return None
    except JWTError:
        raise IncorrectTokenException()
    return payload


async def get_current_user(
    async_db: AsyncSession = Depends(get_async_session),
    token: str = Depends(get_token),
) -> User:
    if token:
        payload = valid_token(token=token)
        user_id: str = payload.get("sub")
        user: User = await UserRepository.find_one_or_none(
            id=int(user_id), session=async_db
        )
        if not user:
            raise UserIsNotPresentException()
        return user
    else:
        raise TokenAbsentException