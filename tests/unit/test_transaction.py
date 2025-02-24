import pytest
from ravenchain.transaction import Transaction
from ravenchain.wallet import Wallet
from datetime import datetime


@pytest.fixture
def wallet():
    w = Wallet()
    w.create_wallet()
    return w


@pytest.fixture
def sample_transaction(wallet):
    recipient = Wallet()
    recipient.create_wallet()
    return Transaction(wallet.address, recipient.address, 10.0)


def test_transaction_creation(sample_transaction):
    """Test basic transaction creation"""
    assert sample_transaction.sender is not None
    assert sample_transaction.recipient is not None
    assert sample_transaction.amount == 10.0
    assert isinstance(sample_transaction.timestamp, datetime)


def test_transaction_to_dict(sample_transaction):
    """Test transaction serialization to dictionary"""
    tx_dict = sample_transaction.to_dict()

    assert isinstance(tx_dict, dict)
    assert "sender" in tx_dict
    assert "recipient" in tx_dict
    assert "amount" in tx_dict
    assert "timestamp" in tx_dict

    assert tx_dict["amount"] == 10.0
    assert isinstance(tx_dict["timestamp"], str)


def test_mining_reward_transaction():
    """Test creation of mining reward transaction"""
    recipient = Wallet()
    recipient.create_wallet()
    reward_amount = 10.0

    transaction = Transaction(None, recipient.address, reward_amount)

    assert transaction.sender is None
    assert transaction.recipient == recipient.address
    assert transaction.amount == reward_amount


def test_invalid_transaction_amount():
    """Test transaction with invalid amount"""
    wallet = Wallet()
    wallet.create_wallet()
    recipient = Wallet()
    recipient.create_wallet()

    with pytest.raises(ValueError):
        Transaction(wallet.address, recipient.address, -10.0)

    with pytest.raises(ValueError):
        Transaction(wallet.address, recipient.address, 0)
