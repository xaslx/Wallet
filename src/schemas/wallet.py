from enum import Enum
from pydantic import BaseModel
from decimal import Decimal




class OperationType(str, Enum):
    DEPOSIT: str = 'DEPOSIT'
    WITHDRAW: str = 'WITHDRAW'

class OperationSchema(BaseModel):
    operationType: OperationType
    amount: Decimal

class Wallet(BaseModel):
    id: int
    user_id: int
    wallet_uuid: str
    balance: Decimal


class WalletCreate(BaseModel):
    user_id: int
    wallet_uuid: str