from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.models.wallet import Wallet


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_wallet(self):
        wallet = Wallet(wallet_id=uuid.uuid4(), balance=0)

        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)

        return wallet

    async def get_for_update(self, wallet_id):

        stmt = select(Wallet).where(Wallet.wallet_id == wallet_id).with_for_update()

        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def get_wallet(self, wallet_id):

        stmt = select(Wallet).where(Wallet.wallet_id == wallet_id)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
