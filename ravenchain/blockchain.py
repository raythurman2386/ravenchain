from datetime import datetime
from .block import Block
from .transaction import Transaction
from .wallet import Wallet

class Blockchain:
    def __init__(self, difficulty=4):
        """
        Initialize the blockchain with a genesis block.
        
        :param difficulty: Mining difficulty (number of leading zeros required in hash)
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10.0
        self.nodes = set()  # For decentralization

    def create_genesis_block(self):
        """
        Create the first block in the chain (genesis block).
        
        :return: A Block object representing the genesis block
        """
        return Block(0, datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        """
        Get the most recent block in the chain.
        
        :return: The latest Block object
        """
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        """
        Add a new transaction to the list of pending transactions.
        
        :param sender: Sender's wallet address
        :param recipient: Recipient's wallet address
        :param amount: Amount to transfer
        :return: Index of the block that will hold this transaction
        """
        transaction = Transaction(sender, recipient, amount)
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self, miner_address):
        """
        Mine pending transactions and add them to a new block.
        
        :param miner_address: Address where the mining reward will be sent
        """
        block = Block(
            len(self.chain),
            datetime.now(),
            self.pending_transactions,
            self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        
        # Reset pending transactions and add mining reward
        self.pending_transactions = [
            Transaction(None, miner_address, self.mining_reward)
        ]

    def is_chain_valid(self):
        """
        Check if the blockchain is valid by verifying all blocks and their links.
        
        :return: True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance(self, address):
        """
        Calculate the balance of a given address.
        
        :param address: Wallet address to check
        :return: Current balance
        """
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if isinstance(transaction, Transaction):
                    if transaction.sender == address:
                        balance -= transaction.amount
                    if transaction.recipient == address:
                        balance += transaction.amount
        return balance
