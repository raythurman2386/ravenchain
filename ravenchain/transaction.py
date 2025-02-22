from datetime import datetime

class Transaction:
    def __init__(self, sender, recipient, amount):
        """
        Initialize a new transaction.
        
        :param sender: Address of the sender (None for mining rewards)
        :param recipient: Address of the recipient
        :param amount: Amount to transfer
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = datetime.now()

    def to_dict(self):
        """
        Convert the transaction to a dictionary format.
        
        :return: Dictionary representation of the transaction
        """
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': str(self.timestamp)
        }
