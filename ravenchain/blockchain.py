from datetime import datetime, timezone
from api.database.models import BlockDB, TransactionDB
from ravenchain.wallet import Wallet
from .block import Block
from .transaction import Transaction


class Blockchain:
    def __init__(self, sessionmaker, difficulty=4, mining_reward=10.0):
        """
        Initialize the blockchain with a genesis block or load from database.

        :param sessionmaker: SQLAlchemy sessionmaker for database operations
        :param difficulty: Mining difficulty (number of leading zeros required in hash)
        :param mining_reward: Reward given to miners for each block
        """
        self.sessionmaker = sessionmaker
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.chain = []
        with self.sessionmaker() as session:
            self.chain = self.load_chain_from_db(session)
            if not self.chain:
                genesis_block = self.create_genesis_block()
                self.chain = [genesis_block]
                self.save_block_to_db(session, genesis_block)
        self.pending_transactions = []

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
        :raises: ValueError if no blocks are found
        """
        if not self.chain:
            with self.sessionmaker() as session:
                self.chain = self.load_chain_from_db(session)
        if not self.chain:
            raise ValueError("No blocks found in the chain")
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
        self.pending_transactions.append(tx)
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self, miner_address):
        """
        Mine pending transactions and add them to a new block, then save to database.

        :param miner_address: Address where the mining reward will be sent
        """
        with self.sessionmaker() as session:
            coinbase_tx = Transaction(None, miner_address, self.mining_reward)
            block_data = [coinbase_tx] + self.pending_transactions
            block = Block(
                len(self.chain),
                datetime.now(timezone.utc),
                block_data,
                self.get_latest_block().hash,
            )
            block.mine_block(self.difficulty)
            self.chain.append(block)
            self.save_block_to_db(session, block)
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

    def load_chain_from_db(self, session):
        """
        Load the blockchain from the database, converting DB models to in-memory models.

        :param session: SQLAlchemy session for database queries
        :return: List of Block objects
        """
        chain = []
        db_blocks = session.query(BlockDB).order_by(BlockDB.index).all()
        for db_block in db_blocks:
            transactions = []
            for db_tx in db_block.transactions:
                tx = Transaction(
                    db_tx.sender, db_tx.recipient, db_tx.amount, signature=db_tx.signature
                )
                tx.timestamp = db_tx.timestamp
                transactions.append(tx)
            block = Block(db_block.index, db_block.timestamp, transactions, db_block.previous_hash)
            block.nonce = db_block.nonce
            block.hash = db_block.hash
            chain.append(block)
        return chain

    def save_block_to_db(self, session, block):
        """
        Save a block and its transactions to the database.

        :param session: SQLAlchemy session for database operations
        :param block: Block object to save
        """
        db_block = BlockDB(
            index=block.index,
            timestamp=block.timestamp,
            previous_hash=block.previous_hash,
            nonce=block.nonce,
            hash=block.hash,
        )
        session.add(db_block)
        session.flush()
        for tx in block.data:
            db_tx = TransactionDB(
                sender=tx.sender,
                recipient=tx.recipient,
                amount=tx.amount,
                timestamp=tx.timestamp,
                signature=tx.signature,
                block_id=db_block.id,
            )
            session.add(db_tx)
        session.commit()
