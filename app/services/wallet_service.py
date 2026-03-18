from fastapi import HTTPException

from app.repositories.wallet_repository import WalletRepository
from app.core.enums import OperationType


class WalletService:
    def __init__(self, wallet_repository: WalletRepository):
        self.wallet_repository = wallet_repository

    async def create_wallet(self):
        wallet = await self.wallet_repository.create_wallet()

        return {"wallet_id": wallet.wallet_id, "balance": wallet.balance}

    async def process_operation(self, wallet_id, operation_type, amount):

        async with self.wallet_repository.session.begin():

            wallet = await self.wallet_repository.get_for_update(wallet_id)

            if wallet is None:
                raise HTTPException(status_code=404, detail="Wallet not found.")

            if operation_type == OperationType.DEPOSIT:
                wallet.balance += amount

            elif operation_type == OperationType.WITHDRAW:
                if wallet.balance < amount:
                    raise HTTPException(status_code=400, detail="Not enough funds!")

                wallet.balance -= amount

            return {"balance": wallet.balance}

    async def get_wallet_balance(self, wallet_id):

        wallet = await self.wallet_repository.get_wallet(wallet_id)

        if wallet is None:
            raise HTTPException(status_code=404, detail="Wallet not found.")

        return {"balance": wallet.balance}
