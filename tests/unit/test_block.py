import pytest
from datetime import datetime, timezone
from ravenchain.transaction import Transaction
from ravenchain.block import Block


def test_block_initialization():
    tx = Transaction("sender", "recipient", 10)
    block = Block(0, data=[tx])
    assert block.index == 0
    assert isinstance(block.timestamp, datetime)
    assert block.data == [tx]
    assert block.previous_hash == "0"
    assert len(block.hash) == 64


def test_block_initialization_with_invalid_index():
    with pytest.raises(ValueError):
        Block(-1)


def test_block_initialization_with_invalid_data():
    with pytest.raises(ValueError):
        Block(0, data=["not a transaction"])


def test_calculate_hash():
    tx = Transaction("sender", "recipient", 10)
    block = Block(0, data=[tx])
    original_hash = block.hash
    block.nonce += 1
    new_hash = block.calculate_hash()
    assert new_hash != original_hash
    assert len(new_hash) == 64


def test_mine_block():
    tx = Transaction("sender", "recipient", 10)
    block = Block(0, data=[tx])
    difficulty = 4
    block.mine_block(difficulty)
    assert block.hash.startswith("0" * difficulty)


def test_to_dict():
    tx = Transaction("sender", "recipient", 10)
    block = Block(0, data=[tx])
    block_dict = block.to_dict()
    assert isinstance(block_dict, dict)
    assert "index" in block_dict
    assert "timestamp" in block_dict
    assert "data" in block_dict
    assert "previous_hash" in block_dict
    assert "nonce" in block_dict
    assert "hash" in block_dict


def test_from_dict():
    tx = Transaction("sender", "recipient", 10)
    original_block = Block(0, data=[tx])
    block_dict = original_block.to_dict()
    reconstructed_block = Block.from_dict(block_dict)

    assert reconstructed_block.index == original_block.index
    assert reconstructed_block.timestamp == original_block.timestamp
    assert reconstructed_block.previous_hash == original_block.previous_hash
    assert reconstructed_block.nonce == original_block.nonce
    assert reconstructed_block.hash == original_block.hash
    assert len(reconstructed_block.data) == len(original_block.data)
