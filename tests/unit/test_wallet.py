import ecdsa
import pytest
from ravenchain.wallet import Wallet
from ravenchain.transaction import Transaction


def test_wallet_creation():
    wallet = Wallet()
    wallet.create_wallet()
    assert wallet.address is not None
    assert len(wallet.address) > 0
    assert wallet.address.startswith("1")  # Bitcoin-style address format


def test_address_generation():
    wallet = Wallet()
    wallet.create_wallet()
    address1 = wallet.address
    address2 = wallet._generate_address()
    assert address1 == address2  # Address should be cached


def test_public_key():
    wallet = Wallet()
    wallet.create_wallet()
    public_key = wallet.public_key
    assert isinstance(public_key, str)  # Changed to str since we're returning hex
    assert len(public_key) == 128  # SECP256k1 public key is 64 bytes = 128 hex chars


def test_wallet_uniqueness():
    wallet1 = Wallet()
    wallet1.create_wallet()
    wallet2 = Wallet()
    wallet2.create_wallet()
    assert wallet1.address != wallet2.address
    assert wallet1.public_key != wallet2.public_key


def test_transaction_signing():
    wallet = Wallet()
    wallet.create_wallet()
    transaction = Transaction(wallet.address, "recipient_address", 100)
    signature = wallet.sign_transaction(transaction)
    assert signature is not None
    assert len(signature) > 0


def test_signature_verification():
    wallet = Wallet()
    wallet.create_wallet()
    transaction = Transaction(wallet.address, "recipient_address", 100)
    signature = wallet.sign_transaction(transaction)

    assert Wallet.verify_signature(wallet.public_key, signature, transaction)

    # Test with incorrect public key
    incorrect_wallet = Wallet()
    incorrect_wallet.create_wallet()
    assert not Wallet.verify_signature(incorrect_wallet.public_key, signature, transaction)


def test_signature_verification_with_tampered_transaction():
    wallet = Wallet()
    wallet.create_wallet()
    transaction = Transaction(wallet.address, "recipient_address", 100)
    signature = wallet.sign_transaction(transaction)

    # Tamper with the transaction
    tampered_transaction = Transaction(wallet.address, "recipient_address", 200)

    assert not Wallet.verify_signature(wallet.public_key, signature, tampered_transaction)


@pytest.mark.parametrize("curve", [ecdsa.SECP256k1, ecdsa.NIST192p, ecdsa.NIST224p])
def test_different_curves(curve):
    class TestWallet(Wallet):
        def __init__(self, curve):
            super().__init__()
            self.create_wallet()
            self._private_key = ecdsa.SigningKey.generate(curve=curve)
            self._public_key = self._private_key.get_verifying_key()
            self._address = self._generate_address()

    wallet = TestWallet(curve)
    assert wallet.address is not None
    assert len(wallet.address) > 0
