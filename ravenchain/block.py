import hashlib
import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        """
        Initialize a block with its attributes.
        
        :param index: The position of the block in the chain
        :param timestamp: The time the block was created
        :param data: The message or data stored in the block
        :param previous_hash: The hash of the previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Added for proof of work
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the hash of the block based on its attributes using SHA-256.
        
        :return: The hash as a hexadecimal string
        """
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        """
        Mine the block by finding a hash that starts with the given number of zeros.
        
        :param difficulty: Number of leading zeros required in the hash
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash
