import pytest
from ravenchain.transaction import Transaction
from datetime import datetime


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
    recipient_address = "test_address"
    reward_amount = 10.0

    transaction = Transaction(None, recipient_address, reward_amount)

    assert transaction.sender is None
    assert transaction.recipient == recipient_address
    assert transaction.amount == reward_amount


def test_invalid_transaction_amount():
    """Test transaction with invalid amount"""
    with pytest.raises(ValueError):
        Transaction("sender", "recipient", -10.0)

    with pytest.raises(ValueError):
        Transaction("sender", "recipient", 0)
