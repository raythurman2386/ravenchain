from fastapi import APIRouter, Depends, HTTPException
from ravenchain.wallet import Wallet
from pydantic import BaseModel

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
async def create_wallet(
    request: WalletCreate, wallet_manager: Wallet = Depends(get_wallet_manager)
):
    try:
        wallet = wallet_manager.create_wallet(passphrase=request.passphrase)
        return {"address": wallet.address, "public_key": wallet.public_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@walletRouter.get("/wallets/{address}")
async def get_wallet_info(address: str, wallet_manager: Wallet = Depends(get_wallet_manager)):
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
