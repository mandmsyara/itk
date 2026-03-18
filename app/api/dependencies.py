from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.repositories.wallet_repository import WalletRepository
from app.services.wallet_service import WalletService


def get_wallet_repository(
    session: AsyncSession = Depends(get_async_session),
) -> WalletRepository:
    return WalletRepository(session)


def get_wallet_service(
    wallet_repository: WalletRepository = Depends(get_wallet_repository),
) -> WalletService:
    return WalletService(wallet_repository)
