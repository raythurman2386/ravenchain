import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database.models import Base
from ravenchain import Blockchain, Wallet, Block, Transaction
from datetime import datetime


# Session-scoped fixture for the in-memory SQLite engine
@pytest.fixture(scope="session")
def test_engine():
    """Create an in-memory SQLite engine for testing"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    return engine


# Session-scoped fixture for the sessionmaker
@pytest.fixture(scope="session")
def test_sessionmaker(test_engine):
    """Create a sessionmaker for the test engine"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Function-scoped fixture for the blockchain with a clean database
@pytest.fixture
def blockchain(test_sessionmaker, test_engine):
    """Create a fresh blockchain instance for testing with a clean database"""
    # Drop and recreate tables to ensure a clean state for each test
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    return Blockchain(test_sessionmaker, difficulty=2)  # Pass sessionmaker to Blockchain


# Fixture for a single test wallet
@pytest.fixture
def wallet():
    """Create a test wallet"""
    return Wallet()


# Fixture for multiple test wallets
@pytest.fixture
def test_wallets():
    """Create multiple test wallets"""
    return [Wallet() for _ in range(3)]


# Fixture for a mined blockchain
@pytest.fixture
def mined_blockchain(blockchain, wallet):
    """Create a blockchain with some mined blocks"""
    # Mine 3 blocks
    for _ in range(3):
        blockchain.mine_pending_transactions(wallet.address)
    return blockchain


# Fixture for a sample transaction
@pytest.fixture
def sample_transaction(test_wallets):
    """Create a sample transaction between two wallets"""
    sender, recipient = test_wallets[0], test_wallets[1]
    return Transaction(sender.address, recipient.address, 10.0)


# Fixture for a sample block
@pytest.fixture
def sample_block():
    """Create a sample block for testing"""
    return Block(index=1, timestamp=datetime.now(), data="Test Block", previous_hash="0000")


# Optional fixture for direct database access
@pytest.fixture
def db_session(test_sessionmaker):
    """Provide a database session for tests"""
    session = test_sessionmaker()
    try:
        yield session
    finally:
        session.close()
