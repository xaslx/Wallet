from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from decimal import Decimal


class Wallet(Base):

    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    wallet_uuid: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 3), default=Decimal(0.0))