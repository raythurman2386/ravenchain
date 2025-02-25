from fastapi import APIRouter, Depends, HTTPException, Request
from api.dependencies import logger, get_blockchain, limiter
from ravenchain.blockchain import Blockchain
from pydantic import BaseModel


class MiningRequest(BaseModel):
    miner_address: str


miningRouter = APIRouter()


@miningRouter.post("/mine")
@limiter.limit("5/minute")  # Strict limit for mining operations
async def mine_block(request: Request, mining_request: MiningRequest, blockchain: Blockchain = Depends(get_blockchain)):
    try:
        blockchain.mine_pending_transactions(mining_request.miner_address)
        return {"message": "Block mined successfully"}
    except Exception as e:
        logger.error(f"Error mining block: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
