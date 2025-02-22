import pytest
from ravenchain.wallet import Wallet
from ravenchain.transaction import Transaction


def test_wallet_creation(wallet):
    """Test wallet initialization"""
    assert wallet.address is not None
    assert len(wallet.address) > 0
    assert wallet.address.startswith("1")  # Bitcoin-style address format


def test_wallet_uniqueness():
    """Test that each wallet gets a unique address"""
    wallet1 = Wallet()
    wallet2 = Wallet()
    assert wallet1.address != wallet2.address


def test_transaction_signing(wallet, sample_transaction):
    """Test transaction signing and verification"""
    # Sign transaction
    signature = wallet.sign_transaction(sample_transaction)
    assert signature is not None

    # Verify signature with correct public key
    assert Wallet.verify_signature(
        wallet.get_public_key(), signature, sample_transaction
    )

    # Verify signature fails with different public key
    different_wallet = Wallet()
    assert not Wallet.verify_signature(
        different_wallet.get_public_key(), signature, sample_transaction
    )


def test_address_generation():
    """Test wallet address generation format"""
    wallet = Wallet()
    address = wallet.address

    # Check address format
    assert isinstance(address, str)
    assert len(address) >= 26  # Standard Bitcoin address length
    assert len(address) <= 35
    assert address.startswith("1")  # Mainnet address

    # Check address uniqueness
    addresses = [Wallet().address for _ in range(10)]
    assert len(set(addresses)) == 10  # All addresses should be unique


def test_public_key_consistency(wallet):
    """Test that public key remains consistent"""
    public_key1 = wallet.get_public_key()
    public_key2 = wallet.get_public_key()
    assert public_key1 == public_key2
