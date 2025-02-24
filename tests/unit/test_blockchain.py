import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database.models import Base
from ravenchain.blockchain import Blockchain
from ravenchain.transaction import Transaction
from ravenchain.wallet import Wallet
from ravenchain.block import Block


@pytest.fixture
def wallet():
    w = Wallet()
    w.create_wallet()
    return w


@pytest.fixture
def db_session():
    # Use SQLite in-memory database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session


@pytest.fixture
def blockchain(db_session):
    return Blockchain(db_session, difficulty=2, mining_reward=10.0)


def test_blockchain_initialization(blockchain):
    assert len(blockchain.chain) == 1
    assert blockchain.difficulty == 2
    assert blockchain.mining_reward == 10.0
    assert len(blockchain.pending_transactions) == 0


def test_create_genesis_block(blockchain):
    genesis_block = blockchain.chain[0]
    assert genesis_block.index == 0
    assert genesis_block.previous_hash == "0"
    assert len(genesis_block.data) == 0


def test_get_latest_block(blockchain):
    latest_block = blockchain.get_latest_block()
    assert latest_block.index == 0
    assert latest_block == blockchain.chain[-1]


def test_add_transaction(blockchain, wallet):
    recipient = Wallet()
    recipient.create_wallet()
    blockchain.add_transaction(wallet.address, recipient.address, 5.0, wallet)
    assert len(blockchain.pending_transactions) == 1
    tx = blockchain.pending_transactions[0]
    assert tx.sender == wallet.address
    assert tx.recipient == recipient.address
    assert tx.amount == 5.0
    assert tx.signature is not None


def test_mine_pending_transactions(blockchain, wallet):
    recipient = Wallet()
    recipient.create_wallet()
    blockchain.add_transaction(wallet.address, recipient.address, 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)
    assert len(blockchain.chain) == 2
    assert len(blockchain.pending_transactions) == 0
    mined_block = blockchain.chain[-1]
    assert len(mined_block.data) == 2  # Coinbase transaction + user transaction


def test_get_balance(blockchain, wallet):
    recipient = Wallet()
    recipient.create_wallet()
    blockchain.add_transaction(wallet.address, recipient.address, 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)
    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward - 5.0
    assert blockchain.get_balance(recipient.address) == 5.0


def test_is_chain_valid(blockchain, wallet):
    recipient = Wallet()
    recipient.create_wallet()
    blockchain.add_transaction(wallet.address, recipient.address, 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)
    wallet_registry = {wallet.address: wallet, recipient.address: recipient}
    assert blockchain.is_chain_valid(wallet_registry)


def test_invalid_chain(blockchain, wallet):
    recipient = Wallet()
    recipient.create_wallet()
    blockchain.add_transaction(wallet.address, recipient.address, 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)
    # Tamper with a transaction
    blockchain.chain[1].data[1].amount = 100.0
    wallet_registry = {wallet.address: wallet, recipient.address: recipient}
    assert not blockchain.is_chain_valid(wallet_registry)


def test_invalid_previous_hash(blockchain):
    miner = Wallet()
    miner.create_wallet()
    blockchain.mine_pending_transactions(miner.address)
    blockchain.chain[1].previous_hash = "invalid_hash"
    assert not blockchain.is_chain_valid({})


def test_invalid_block_hash(blockchain):
    miner = Wallet()
    miner.create_wallet()
    blockchain.mine_pending_transactions(miner.address)
    blockchain.chain[1].hash = "invalid_hash"
    assert not blockchain.is_chain_valid({})


def test_mining_reward(blockchain, wallet):
    blockchain.mine_pending_transactions(wallet.address)
    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward
    blockchain.mine_pending_transactions(wallet.address)
    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward * 2
