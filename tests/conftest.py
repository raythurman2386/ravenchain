import pytest
from ravenchain.blockchain import Blockchain
from ravenchain.wallet import Wallet
from ravenchain.block import Block
from ravenchain.transaction import Transaction
from datetime import datetime


@pytest.fixture
def blockchain():
    """Create a fresh blockchain instance for testing"""
    return Blockchain(difficulty=2)  # Lower difficulty for faster tests


@pytest.fixture
def wallet():
    """Create a test wallet"""
    return Wallet()


@pytest.fixture
def test_wallets():
    """Create multiple test wallets"""
    return [Wallet() for _ in range(3)]


@pytest.fixture
def mined_blockchain(blockchain, wallet):
    """Create a blockchain with some mined blocks"""
    # Mine 3 blocks
    for _ in range(3):
        blockchain.mine_pending_transactions(wallet.address)
    return blockchain


@pytest.fixture
def sample_transaction(test_wallets):
    """Create a sample transaction between two wallets"""
    sender, recipient = test_wallets[0], test_wallets[1]
    return Transaction(sender.address, recipient.address, 10.0)


@pytest.fixture
def sample_block():
    """Create a sample block for testing"""
    return Block(
        index=1, timestamp=datetime.now(), data="Test Block", previous_hash="0000"
    )
