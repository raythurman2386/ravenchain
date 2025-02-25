from fastapi import APIRouter, Depends, HTTPException, Request
from ravenchain.wallet import Wallet
from pydantic import BaseModel
from api.dependencies import limiter

walletRouter = APIRouter()


class WalletCreate(BaseModel):
    passphrase: str | None = None


def get_wallet_manager():
    try:
        return Wallet()
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Wallet manager initialization failed: {str(e)}"
        )


@walletRouter.post("/wallets")
@limiter.limit("20/minute")
async def create_wallet(
    request: Request, wallet_data: WalletCreate, wallet_manager: Wallet = Depends(get_wallet_manager)
):
    try:
        wallet = wallet_manager.create_wallet(wallet_data.passphrase)
        return {"address": wallet.address, "public_key": wallet.public_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@walletRouter.get("/wallets/{address}")
@limiter.limit("30/minute")
async def get_wallet_info(
    request: Request, address: str, wallet_manager: Wallet = Depends(get_wallet_manager)
):
    try:
        wallet = wallet_manager.get_wallet(address)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return {
            "address": wallet.address,
            "public_key": wallet.public_key,
            "balance": wallet_manager.get_balance(address),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
