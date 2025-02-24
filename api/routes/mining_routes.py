from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import logger, get_blockchain
from ravenchain.blockchain import Blockchain
from pydantic import BaseModel


class MiningRequest(BaseModel):
    miner_address: str


miningRouter = APIRouter()


@miningRouter.post("/mine")
async def mine_block(request: MiningRequest, blockchain: Blockchain = Depends(get_blockchain)):
    try:
        blockchain.mine_pending_transactions(request.miner_address)
        return {"message": "Block mined successfully"}
    except Exception as e:
        logger.error(f"Error mining block: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
