import pytest
from datetime import datetime, timezone
from ravenchain.blockchain import Blockchain
from ravenchain.transaction import Transaction
from ravenchain.wallet import Wallet
from ravenchain.block import Block


@pytest.fixture
def blockchain():
    return Blockchain(difficulty=2, mining_reward=10.0)


@pytest.fixture
def wallet():
    return Wallet()


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
    recipient = Wallet().address
    blockchain.add_transaction(wallet.address, recipient, 5.0, wallet)
    assert len(blockchain.pending_transactions) == 1
    tx = blockchain.pending_transactions[0]
    assert tx.sender == wallet.address
    assert tx.recipient == recipient
    assert tx.amount == 5.0
    assert tx.signature is not None


def test_mine_pending_transactions(blockchain, wallet):
    blockchain.add_transaction(wallet.address, "recipient", 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)
    assert len(blockchain.chain) == 2
    assert len(blockchain.pending_transactions) == 0
    mined_block = blockchain.chain[-1]
    assert len(mined_block.data) == 2  # Coinbase transaction + user transaction


def test_get_balance(blockchain, wallet):
    recipient = Wallet().address
    blockchain.add_transaction(wallet.address, recipient, 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)

    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward - 5.0
    assert blockchain.get_balance(recipient) == 5.0


def test_is_chain_valid(blockchain, wallet):
    recipient = Wallet().address
    blockchain.add_transaction(wallet.address, recipient, 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)

    wallet_registry = {wallet.address: wallet, recipient: Wallet()}
    assert blockchain.is_chain_valid(wallet_registry)


def test_invalid_chain(blockchain, wallet):
    recipient = Wallet().address
    blockchain.add_transaction(wallet.address, recipient, 5.0, wallet)
    blockchain.mine_pending_transactions(wallet.address)

    # Tamper with a transaction
    blockchain.chain[1].data[1].amount = 100.0

    wallet_registry = {wallet.address: wallet, recipient: Wallet()}
    assert not blockchain.is_chain_valid(wallet_registry)


def test_invalid_previous_hash(blockchain):
    blockchain.mine_pending_transactions(Wallet().address)
    blockchain.chain[1].previous_hash = "invalid_hash"
    assert not blockchain.is_chain_valid({})


def test_invalid_block_hash(blockchain):
    blockchain.mine_pending_transactions(Wallet().address)
    blockchain.chain[1].hash = "invalid_hash"
    assert not blockchain.is_chain_valid({})


def test_mining_reward(blockchain, wallet):
    blockchain.mine_pending_transactions(wallet.address)
    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward

    blockchain.mine_pending_transactions(wallet.address)
    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward * 2
