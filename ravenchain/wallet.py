import hashlib
import ecdsa
import base58
import os


class Wallet:
    def __init__(self):
        """Initialize a new wallet with a key pair"""
        self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self._public_key = self._private_key.get_verifying_key()
        self.address = self._generate_address()

    def _generate_address(self):
        """
        Generate a wallet address from the public key.
        Similar to Bitcoin address generation (simplified).

        :return: Wallet address as a string
        """
        # Get the public key in bytes
        public_key_bytes = self._public_key.to_string()

        # Perform SHA-256 hashing
        sha256_hash = hashlib.sha256(public_key_bytes).digest()

        # Perform RIPEMD-160 hashing
        ripemd160_hash = hashlib.new("ripemd160")
        ripemd160_hash.update(sha256_hash)

        # Add version byte in front (0x00 for mainnet)
        version_hash = b"\x00" + ripemd160_hash.digest()

        # Perform double SHA-256 hashing
        double_sha256 = hashlib.sha256(hashlib.sha256(version_hash).digest()).digest()

        # Add checksum to version_hash
        binary_address = version_hash + double_sha256[:4]

        # Encode to base58
        address = base58.b58encode(binary_address).decode("utf-8")
        return address

    def sign_transaction(self, transaction):
        """
        Sign a transaction with the wallet's private key.

        :param transaction: Transaction to sign
        :return: Signature as bytes
        """
        transaction_string = (
            f"{transaction.sender}{transaction.recipient}{transaction.amount}"
        )
        return self._private_key.sign(transaction_string.encode())

    def get_public_key(self):
        """
        Get the public key.

        :return: Public key as bytes
        """
        return self._public_key.to_string()

    @staticmethod
    def verify_signature(public_key, signature, transaction):
        """
        Verify a transaction signature.

        :param public_key: Public key bytes
        :param signature: Signature bytes
        :param transaction: Transaction to verify
        :return: True if signature is valid, False otherwise
        """
        verifying_key = ecdsa.VerifyingKey.from_string(
            public_key, curve=ecdsa.SECP256k1
        )
        transaction_string = (
            f"{transaction.sender}{transaction.recipient}{transaction.amount}"
        )
        try:
            return verifying_key.verify(signature, transaction_string.encode())
        except:
            return False
