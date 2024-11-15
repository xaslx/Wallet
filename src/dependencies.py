from fastapi import Depends, Path
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.dependencies import get_current_user
from src.models.user import User
from src.schemas.wallet import Wallet
from src.repositories.wallet import WalletRepository
from exceptions import WalletNotFound
from typing import Annotated


async def get_wallet(
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)], 
        wallet_uuid: Annotated[str, Path()]
    ) -> Wallet:

    wallet: Wallet = await WalletRepository.find_one_or_none(session=session, wallet_uuid=wallet_uuid, user_id=user.id)
    if wallet:
        return wallet
    else:
        raise WalletNotFound()