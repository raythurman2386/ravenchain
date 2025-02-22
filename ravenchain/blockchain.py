from datetime import datetime
from .block import Block
from .transaction import Transaction


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

    def create_genesis_block(self):
        """
        Create the first block in the chain (genesis block).

        :return: A Block object representing the genesis block
        """
        return Block(0, datetime.now(), [], "0")

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
        :raises ValueError: If sender has insufficient balance
        """
        # Mining rewards don't need balance check
        if sender is not None:
            balance = self.get_balance(sender)
            if balance < amount:
                raise ValueError(
                    f"Insufficient balance. Has: {balance}, Needs: {amount}"
                )

        transaction = Transaction(sender, recipient, amount)
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self, miner_address):
        """
        Mine pending transactions and add them to a new block.

        :param miner_address: Address where the mining reward will be sent
        """
        # Create a new block with pending transactions
        block = Block(
            len(self.chain),
            datetime.now(),
            self.pending_transactions,
            self.get_latest_block().hash,
        )

        # Mine the block
        block.mine_block(self.difficulty)

        # Add the block to the chain
        self.chain.append(block)

        # Clear pending transactions and add mining reward for next block
        self.pending_transactions = [
            Transaction(None, miner_address, self.mining_reward)
        ]

    def get_balance(self, address):
        """
        Calculate the balance of a given address.

        :param address: Wallet address to check
        :return: Current balance
        """
        balance = 0

        # Process transactions in order
        for i, block in enumerate(self.chain):
            if not isinstance(block.data, list):
                continue

            for transaction in block.data:
                if not isinstance(transaction, Transaction):
                    continue

                # Process regular transactions
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    if transaction.sender is None:  # Mining reward
                        # Only count mining rewards from blocks that have been confirmed
                        if i < len(self.chain) - 1:
                            balance += transaction.amount
                    else:  # Regular transaction
                        # Regular transactions are counted immediately
                        balance += transaction.amount

        return balance

    def is_chain_valid(self):
        """
        Check if the blockchain is valid by verifying all blocks and their transactions.

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

            # Verify transactions in the current block
            if isinstance(current_block.data, list):
                # Calculate balances from previous blocks
                balances = {}
                for prev_block in self.chain[:i]:
                    if not isinstance(prev_block.data, list):
                        continue
                    for tx in prev_block.data:
                        if not isinstance(tx, Transaction):
                            continue
                        if tx.sender:
                            balances[tx.sender] = balances.get(tx.sender, 0) - tx.amount
                        balances[tx.recipient] = (
                            balances.get(tx.recipient, 0) + tx.amount
                        )

                # Validate transactions within the current block sequentially
                for tx in current_block.data:
                    if not isinstance(tx, Transaction):
                        continue
                    if tx.sender is None:  # Mining reward
                        balances[tx.recipient] = (
                            balances.get(tx.recipient, 0) + tx.amount
                        )
                        continue
                    sender_balance = balances.get(tx.sender, 0)
                    if sender_balance < tx.amount:
                        return False
                    balances[tx.sender] = sender_balance - tx.amount
                    balances[tx.recipient] = balances.get(tx.recipient, 0) + tx.amount

        return True
