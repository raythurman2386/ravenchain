from datetime import datetime, timezone


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        """Initialize a new transaction"""
        if amount <= 0:
            raise ValueError("Transaction amount must be positive")
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = datetime.now(timezone.utc)
        self.signature = signature

    def to_dict(self):
        """Convert the transaction to a dictionary format"""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "signature": self.signature.hex() if self.signature else None,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a transaction from a dictionary"""
        timestamp = datetime.fromisoformat(data["timestamp"])
        signature = bytes.fromhex(data["signature"]) if data["signature"] else None
        return cls(data["sender"], data["recipient"], data["amount"], signature)

    def __repr__(self):
        return (
            f"Transaction(sender={self.sender}, recipient={self.recipient}, "
            f"amount={self.amount}, timestamp={self.timestamp}, "
            f"signature={self.signature.hex() if self.signature else None})"
        )
