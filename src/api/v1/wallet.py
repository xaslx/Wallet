import asyncio
from decimal import Decimal
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.models.user import User
from src.schemas.wallet import WalletCreate, Wallet
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import get_async_session
from src.repositories.wallet import WalletRepository
from uuid import uuid4, UUID
from exceptions import NotEnoughMoney
from src.schemas.wallet import OperationSchema, OperationType
from src.dependencies import get_wallet



router: APIRouter = APIRouter(tags=['Кошелек'])




@router.post('/', status_code=201)
async def create_wallet(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Wallet:
    
    wallet_uuid: UUID = uuid4()
    new_wallet: WalletCreate = WalletCreate(user_id=user.id, wallet_uuid=str(wallet_uuid))
    wallet: Wallet = await WalletRepository.add(session=session, **new_wallet.model_dump()) 
    return wallet
    

@router.get('/', status_code=201)
async def get_all_wallets(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[Wallet]:

    wallet: list[Wallet] = await WalletRepository.find_all(session=session, user_id=user.id) 
    return wallet


@router.get('/{wallet_uuid}', status_code=200)
async def get_balance(
    wallet: Annotated[Wallet, Depends(get_wallet)],
    ) -> JSONResponse:

    return JSONResponse(content={'balance': str(wallet.balance)})


@router.delete('/{wallet_uuid}', status_code=200)
async def delete_wallet(
    wallet: Annotated[Wallet, Depends(get_wallet)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
    ) -> JSONResponse:

    await WalletRepository.delete(session=session, id=wallet.id)
    return JSONResponse(content={'detail': 'Кошелек был удален'})


@router.post('/{wallet_uuid}/operation', status_code=200)
async def wallet_operation(
    wallet: Annotated[Wallet, Depends(get_wallet)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    operation: OperationSchema
) -> JSONResponse:

    if operation.operationType == OperationType.DEPOSIT:
        new_balance: Decimal = Decimal(wallet.balance) + operation.amount
        await WalletRepository.update(session=session, id=wallet.id, balance=new_balance)
      

    if operation.operationType == OperationType.WITHDRAW:
        new_balance: Decimal = Decimal(wallet.balance) - operation.amount
        if new_balance < 0:
            raise NotEnoughMoney()
        await WalletRepository.update(session=session, id=wallet.id, balance=new_balance)

    return JSONResponse(content={'new_balance': str(new_balance)})


