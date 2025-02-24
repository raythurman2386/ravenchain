import hashlib
import ecdsa
import base58
import json
from typing import Optional, Dict


class Wallet:
    _wallets: Dict[str, "Wallet"] = {}

    def __init__(self):
        """Initialize a new wallet with a key pair"""
        self._private_key = None
        self._public_key = None
        self._address = None

    def create_wallet(self, passphrase: Optional[str] = None) -> "Wallet":
        """Create a new wallet with an optional passphrase"""
        if passphrase:
            # Use passphrase to generate deterministic private key
            seed = hashlib.sha256(passphrase.encode()).digest()
            self._private_key = ecdsa.SigningKey.from_string(seed, curve=ecdsa.SECP256k1)
        else:
            # Generate random private key
            self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

        self._public_key = self._private_key.get_verifying_key()
        self._address = self._generate_address()

        # Store the wallet
        Wallet._wallets[self._address] = self
        return self

    def _generate_address(self):
        """Generate and cache a wallet address from the public key"""
        if self._address and self._public_key:
            return self._address
        if not self._public_key:
            raise ValueError("Wallet not initialized. Call create_wallet first.")

        public_key_bytes = self._public_key.to_string()
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new("ripemd160")
        ripemd160_hash.update(sha256_hash)
        version_hash = b"\x00" + ripemd160_hash.digest()
        double_sha256 = hashlib.sha256(hashlib.sha256(version_hash).digest()).digest()
        binary_address = version_hash + double_sha256[:4]
        self._address = base58.b58encode(binary_address).decode("utf-8")
        return self._address

    def sign_transaction(self, transaction):
        """Sign a transaction with the wallet's private key"""
        if not self._private_key:
            raise ValueError("Wallet not initialized. Call create_wallet first.")
        transaction_string = f"{transaction.sender}{transaction.recipient}{transaction.amount}"
        return self._private_key.sign(transaction_string.encode())

    @property
    def address(self):
        """Get the wallet address"""
        if not self._address:
            raise ValueError("Wallet not initialized. Call create_wallet first.")
        return self._address

    @property
    def public_key(self):
        """Get the public key as hex string"""
        if not self._public_key:
            raise ValueError("Wallet not initialized. Call create_wallet first.")
        return self._public_key.to_string().hex()

    def get_wallet(self, address: str) -> Optional["Wallet"]:
        """Get a wallet by address"""
        return Wallet._wallets.get(address)

    def get_balance(self, address: str) -> float:
        """Get the balance for a wallet address"""
        # TODO: Implement balance calculation from blockchain
        return 0.0

    @staticmethod
    def verify_signature(public_key, signature, transaction):
        """Verify a transaction signature"""
        verifying_key = ecdsa.VerifyingKey.from_string(
            bytes.fromhex(public_key), curve=ecdsa.SECP256k1
        )
        transaction_string = f"{transaction.sender}{transaction.recipient}{transaction.amount}"
        try:
            return verifying_key.verify(signature, transaction_string.encode())
        except ecdsa.BadSignatureError:
            return False
