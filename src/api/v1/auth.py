from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from exceptions import UserAlreadyExistsException, UserNotFound
from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserInDB, UserSchema, UserRegister, UserLogin



router: APIRouter = APIRouter(
    tags=['Аутентификация и Авторизация']
)



@router.post('/register', status_code=201)
async def rigister_user(
    user: UserRegister,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserSchema:

    exist_user: User = await UserRepository.find_one_or_none(
        session=session, username=user.username
    )

    if exist_user:
        raise UserAlreadyExistsException
    
    hashed_password: str = get_password_hash(user.password)
    user_in_db: UserInDB = UserInDB(username=user.username, hashed_password=hashed_password)
    new_user: User = await UserRepository.add(
        session=session,
        **user_in_db.model_dump()
    )
    return new_user


@router.post('/login', status_code=200)
async def login_user(
    response: Response,
    user: UserLogin,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    
    user: User = await authenticate_user(user.username, user.password, async_db=session)

    if not user:
        raise UserNotFound()

    access_token: str = create_access_token({'sub': str(user.id)})
    response.set_cookie(
        'user_access_token', access_token, httponly=True
    )
    return access_token




@router.post('/logout', status_code=200)
async def logout_user(
    response: Response,
    request: Request,
):
    cookies: str | None = request.cookies.get('user_access_token')
    if cookies:
        response.delete_cookie(key='user_access_token')