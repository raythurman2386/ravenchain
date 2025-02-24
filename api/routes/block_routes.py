from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import logger, get_blockchain
from ravenchain.blockchain import Blockchain


blockRouter = APIRouter()


@blockRouter.get("/blocks")
async def get_all_blocks(blockchain: Blockchain = Depends(get_blockchain)):
    """Get all blocks in the blockchain"""
    try:
        return [block.to_dict() for block in blockchain.chain]
    except Exception as e:
        logger.error(f"Error getting blocks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@blockRouter.get("/blocks/latest")
async def get_latest_block(blockchain: Blockchain = Depends(get_blockchain)):
    """Get the most recent block in the chain"""
    try:
        latest = blockchain.get_latest_block()
        if not latest:
            raise HTTPException(status_code=404, detail="Block not found")
        return latest.to_dict()
    except ValueError as e:
        logger.error(f"Error getting latest block: {str(e)}")
        raise HTTPException(status_code=404, detail="Block not found")
    except Exception as e:
        logger.error(f"Error getting latest block: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@blockRouter.get("/blocks/{block_hash}")
async def get_block(block_hash: str, blockchain: Blockchain = Depends(get_blockchain)):
    """Get a specific block by its hash"""
    try:
        for block in blockchain.chain:
            if block.hash == block_hash:
                return block.to_dict()
        raise HTTPException(status_code=404, detail="Block not found")
    except Exception as e:
        logger.error(f"Error getting block {block_hash}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
