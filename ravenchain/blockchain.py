from datetime import datetime, timezone

from ravenchain.wallet import Wallet
from .block import Block
from .transaction import Transaction


class Blockchain:
    def __init__(self, difficulty=4, mining_reward=10.0):
        """
        Initialize the blockchain with a genesis block.

        :param difficulty: Mining difficulty (number of leading zeros required in hash)
        :param mining_reward: Reward given to miners for each block
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = mining_reward

    def create_genesis_block(self):
        """
        Create the first block in the chain (genesis block).

        :return: A Block object representing the genesis block
        """
        return Block(0, datetime.now(timezone.utc), [], "0")

    def get_latest_block(self):
        """
        Get the most recent block in the chain.

        :return: The latest Block object
        """
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount, wallet=None):
        """
        Add a transaction to the pending pool.

        :param sender: Address of the sender
        :param recipient: Address of the recipient
        :param amount: Amount to transfer
        :param wallet: Optional wallet to sign the transaction
        :return: Index of the block that will include this transaction
        """
        tx = Transaction(sender, recipient, amount)
        if wallet and sender == wallet.address:
            tx.signature = wallet.sign_transaction(tx)
        # Optional: Add validation (e.g., check balance)
        self.pending_transactions.append(tx)
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self, miner_address):
        """
        Mine pending transactions and add them to a new block.

        :param miner_address: Address where the mining reward will be sent
        """
        # Create coinbase transaction for mining reward
        coinbase_tx = Transaction(None, miner_address, self.mining_reward)
        # Include coinbase and pending transactions in the block
        block_data = [coinbase_tx] + self.pending_transactions
        block = Block(
            len(self.chain),
            datetime.now(timezone.utc),
            block_data,
            self.get_latest_block().hash,
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)
        # Clear pending transactions
        self.pending_transactions = []

    def get_balance(self, address):
        """
        Calculate the balance of a given address.

        :param address: Wallet address to check
        :return: Current balance
        """
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        return balance

    def is_chain_valid(self, wallet_registry):
        """
        Verify the integrity of the blockchain.

        :param wallet_registry: Dictionary mapping addresses to wallets for signature verification
        :return: True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != self.chain[i - 1].hash:
                return False
            for tx in current.data:
                if tx.signature and tx.sender:
                    if tx.sender not in wallet_registry:
                        return False
                    public_key = wallet_registry[tx.sender].public_key
                    if not Wallet.verify_signature(public_key, tx.signature, tx):
                        return False
        return True
