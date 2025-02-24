from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.dependencies import blockchain
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
async def get_all_transactions(blockchain: Blockchain = Depends(get_blockchain)):
    transactions = []
    for block in blockchain.chain:
        transactions.extend(block.transactions)
    return transactions


@transactionRouter.post("/transactions")
async def create_transaction(
    request: CreateTransactionRequest, blockchain: Blockchain = Depends(get_blockchain)
):
    try:
        transaction = Transaction(
            request.sender_address,
            request.recipient_address,
            request.amount,
            request.sender_private_key,
        )
        blockchain.add_transaction_to_pool(transaction)
        return {"message": "Transaction added to the pool"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
