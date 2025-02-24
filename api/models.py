from pydantic import BaseModel
from typing import List


class TransactionBase(BaseModel):
    sender: str
    recipient: str
    amount: float
    timestamp: str
    signature: str


class Transaction(TransactionBase):
    id: int
    block_id: int


class BlockBase(BaseModel):
    index: int
    timestamp: str
    previous_hash: str
    nonce: int
    hash: str


class Block(BlockBase):
    id: int
    transactions: List[TransactionBase]
