from uuid import UUID
from fastapi import APIRouter, Depends

from app.schemas.wallet import OperationRequest
from app.services.wallet_service import WalletService
from app.api.dependencies import get_wallet_service

router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])


@router.post("/")
async def create_wallet(wallet_service: WalletService = Depends(get_wallet_service)):
    return await wallet_service.create_wallet()


@router.post("/{wallet_id}/operation")
async def wallet_operation(
    wallet_id: UUID,
    data: OperationRequest,
    wallet_service: WalletService = Depends(get_wallet_service),
):

    return await wallet_service.process_operation(
        wallet_id, data.operation_type, data.amount
    )


@router.get("/{wallet_id}")
async def wallet_balance(
    wallet_id: UUID, wallet_service: WalletService = Depends(get_wallet_service)
):
    return await wallet_service.get_wallet_balance(wallet_id)
