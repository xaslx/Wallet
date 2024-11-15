from src.repositories.sqlalchemy import SQLAlchemyRepository
from src.models.wallet import Wallet




class WalletRepository(SQLAlchemyRepository):
    model: Wallet = Wallet


