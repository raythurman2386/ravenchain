import hashlib
from datetime import datetime, timezone

from ravenchain.transaction import Transaction


class Block:
    def __init__(self, index, timestamp=None, data=None, previous_hash=None):
        """Initialize a block with its attributes"""
        if index is None or index < 0:
            raise ValueError("Block index must be a non-negative integer")
        if not isinstance(data, list) or not all(isinstance(tx, Transaction) for tx in data):
            raise ValueError("Block data must be a list of Transaction objects")

        self.index = index
        self.timestamp = timestamp if timestamp else datetime.now(timezone.utc)
        self.data = data if data is not None else []
        self.previous_hash = previous_hash if previous_hash is not None else "0"
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the hash of the block using SHA-256"""
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        """Mine the block by finding a hash with the required number of leading zeros"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

    def to_dict(self):
        """Convert the block to a dictionary format"""
        return {
            "index": self.index,
            "timestamp": self.timestamp.isoformat(),
            "data": [tx.to_dict() for tx in self.data],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a block from a dictionary"""
        timestamp = datetime.fromisoformat(data["timestamp"])
        transactions = [Transaction.from_dict(tx) for tx in data["data"]]
        block = cls(data["index"], timestamp, transactions, data["previous_hash"])
        block.nonce = data["nonce"]
        block.hash = data["hash"]
        return block
