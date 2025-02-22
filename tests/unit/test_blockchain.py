import pytest
from ravenchain.blockchain import Blockchain
from ravenchain.transaction import Transaction
from ravenchain.wallet import Wallet


def test_create_blockchain():
    blockchain = Blockchain()
    assert len(blockchain.chain) == 1
    assert blockchain.difficulty == 4
    assert blockchain.mining_reward == 10.0
    genesis_block = blockchain.chain[0]
    assert genesis_block.index == 0
    assert genesis_block.previous_hash == "0"
    assert genesis_block.data == []
    assert genesis_block.hash == genesis_block.calculate_hash()


def test_add_transaction():
    blockchain = Blockchain()
    wallet1 = Wallet()
    wallet2 = Wallet()

    blockchain.mine_pending_transactions(wallet1.address)  # Block 1
    blockchain.mine_pending_transactions(wallet1.address)  # Block 2

    initial_balance_wallet1 = blockchain.get_balance(wallet1.address)
    assert initial_balance_wallet1 == blockchain.mining_reward

    blockchain.add_transaction(wallet1.address, wallet2.address, 5.0)
    blockchain.mine_pending_transactions(wallet1.address)  # Block 3 only

    final_balance_wallet1 = blockchain.get_balance(wallet1.address)
    final_balance_wallet2 = blockchain.get_balance(wallet2.address)

    assert (
        final_balance_wallet1
        == initial_balance_wallet1 - 5.0 + blockchain.mining_reward
    )
    assert final_balance_wallet2 == 5.0


def test_mine_pending_transactions():
    blockchain = Blockchain()
    wallet = Wallet()

    blockchain.mine_pending_transactions(wallet.address)  # Block 1
    assert blockchain.get_balance(wallet.address) == 0

    blockchain.mine_pending_transactions(wallet.address)  # Block 2
    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward

    blockchain.mine_pending_transactions(wallet.address)  # Block 3
    assert blockchain.get_balance(wallet.address) == 2 * blockchain.mining_reward

    assert len(blockchain.pending_transactions) == 1


def test_get_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    blockchain.mine_pending_transactions(wallet.address)  # Block 1
    assert blockchain.get_balance(wallet.address) == 0

    blockchain.mine_pending_transactions(wallet.address)  # Block 2
    assert blockchain.get_balance(wallet.address) == blockchain.mining_reward

    blockchain.mine_pending_transactions(wallet.address)  # Block 3
    assert blockchain.get_balance(wallet.address) == 2 * blockchain.mining_reward


def test_invalid_transaction():
    blockchain = Blockchain()
    wallet1 = Wallet()
    wallet2 = Wallet()

    with pytest.raises(ValueError, match="Insufficient balance"):
        blockchain.add_transaction(wallet1.address, wallet2.address, 100.0)

    blockchain.mine_pending_transactions(wallet1.address)  # Block 1
    blockchain.mine_pending_transactions(
        wallet1.address
    )  # Block 2 confirms Block 1 reward

    with pytest.raises(ValueError, match="Insufficient balance"):
        blockchain.add_transaction(
            wallet1.address, wallet2.address, blockchain.mining_reward + 1
        )


def test_chain_validity():
    blockchain = Blockchain()
    wallet = Wallet()

    blockchain.mine_pending_transactions(wallet.address)  # Block 1
    blockchain.mine_pending_transactions(
        wallet.address
    )  # Block 2 confirms Block 1 reward

    assert blockchain.is_chain_valid()

    if blockchain.chain[1].data:
        blockchain.chain[1].data[0].amount = 1000
    assert not blockchain.is_chain_valid()

    blockchain = Blockchain()
    blockchain.mine_pending_transactions(wallet.address)
    blockchain.chain[1].hash = "invalid_hash"
    assert not blockchain.is_chain_valid()

    blockchain = Blockchain()
    blockchain.mine_pending_transactions(wallet.address)
    blockchain.chain[1].previous_hash = "invalid_previous_hash"
    assert not blockchain.is_chain_valid()
