import hashlib
import ecdsa
import base58


class Wallet:
    def __init__(self):
        """Initialize a new wallet with a key pair"""
        self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self._public_key = self._private_key.get_verifying_key()
        self._address = None
        self.address = self._generate_address()

    def _generate_address(self):
        """Generate and cache a wallet address from the public key"""
        if self._address:
            return self._address
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
        transaction_string = (
            f"{transaction.sender}{transaction.recipient}{transaction.amount}"
        )
        return self._private_key.sign(transaction_string.encode())

    @property
    def public_key(self):
        """Get the public key as bytes"""
        return self._public_key.to_string()

    @staticmethod
    def verify_signature(public_key, signature, transaction):
        """Verify a transaction signature"""
        verifying_key = ecdsa.VerifyingKey.from_string(
            public_key, curve=ecdsa.SECP256k1
        )
        transaction_string = (
            f"{transaction.sender}{transaction.recipient}{transaction.amount}"
        )
        try:
            return verifying_key.verify(signature, transaction_string.encode())
        except ecdsa.BadSignatureError:
            return False
