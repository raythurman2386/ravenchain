from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from api.dependencies import blockchain, limiter
from ravenchain.blockchain import Blockchain
from ravenchain.transaction import Transaction

transactionRouter = APIRouter()


class CreateTransactionRequest(BaseModel):
    sender_address: str
    recipient_address: str
    amount: float
    sender_private_key: str


def get_blockchain():
    if not blockchain:
        raise HTTPException(status_code=503, detail="Blockchain not initialized")
    return blockchain


@transactionRouter.get("/transactions")
@limiter.limit("30/minute")
async def get_all_transactions(request: Request, blockchain: Blockchain = Depends(get_blockchain)):
    try:
        return blockchain.get_pending_transactions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@transactionRouter.post("/transactions")
@limiter.limit("10/minute")  # Lower limit for creating transactions
async def create_transaction(
    request: Request,
    tx_request: CreateTransactionRequest,
    blockchain: Blockchain = Depends(get_blockchain),
):
    try:
        transaction = Transaction(
            tx_request.sender_address, tx_request.recipient_address, tx_request.amount
        )
        transaction.sign_transaction(tx_request.sender_private_key)
        blockchain.add_pending_transaction(transaction)
        return {"message": "Transaction added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
