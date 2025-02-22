import pytest
from ravenchain.block import Block
from datetime import datetime


def test_block_creation(sample_block):
    """Test basic block creation"""
    assert sample_block.index == 1
    assert isinstance(sample_block.timestamp, datetime)
    assert sample_block.data == "Test Block"
    assert sample_block.previous_hash == "0000"
    assert sample_block.hash is not None


def test_block_hash_calculation():
    """Test that block hash is calculated correctly"""
    block = Block(1, datetime.now(), "Test Data", "0000")
    initial_hash = block.hash

    # Hash should be a string of 64 characters (SHA-256)
    assert isinstance(block.hash, str)
    assert len(block.hash) == 64

    # Hash should be deterministic
    assert block.hash == block.calculate_hash()

    # Hash should change when data changes
    block.data = "Modified Data"
    assert block.calculate_hash() != initial_hash


def test_block_mining():
    """Test block mining with proof of work"""
    block = Block(1, datetime.now(), "Test Data", "0000")
    difficulty = 2
    block.mine_block(difficulty)

    # Hash should start with the required number of zeros
    assert block.hash.startswith("0" * difficulty)

    # Nonce should have been incremented
    assert block.nonce > 0


def test_invalid_block_parameters():
    """Test block creation with invalid parameters"""
    with pytest.raises(Exception):
        Block(None, datetime.now(), "Test", "0000")

    with pytest.raises(Exception):
        Block(-1, datetime.now(), "Test", "0000")
