#!/usr/bin/env python3
"""
Generate test data for RavenChain development and testing.
Creates wallets, transactions, and mines blocks.
"""
import random
from pathlib import Path
from config.logging import setup_logging
from ravenchain.blockchain import Blockchain
from ravenchain.wallet import Wallet

logger = setup_logging("ravenchain.testdata")


def generate_test_data(
    num_wallets: int = 5,
    num_transactions: int = 20,
    min_amount: float = 0.1,
    max_amount: float = 10.0,
):
    try:
        # Initialize blockchain
        blockchain = Blockchain(difficulty=2)
        wallets = []

        # Create wallets
        logger.info("Creating test wallets", count=num_wallets)
        for i in range(num_wallets):
            wallet = Wallet()
            wallets.append(wallet)
            logger.debug(f"Created wallet {i+1}", address=wallet.address)

        # Generate transactions
        logger.info("Generating test transactions", count=num_transactions)
        for _ in range(num_transactions):
            sender = random.choice(wallets)
            receiver = random.choice([w for w in wallets if w != sender])
            amount = random.uniform(min_amount, max_amount)

            blockchain.add_transaction(sender.address, receiver.address, amount, wallet=sender)

            # Mine a block after every few transactions
            if random.random() < 0.3:  # 30% chance to mine
                miner = random.choice(wallets)
                blockchain.mine_pending_transactions(miner.address)
                logger.info("Mined a new block", miner=miner.address)

        # Mine any remaining transactions
        if blockchain.pending_transactions:
            miner = random.choice(wallets)
            blockchain.mine_pending_transactions(miner.address)
            logger.info("Mined final block", miner=miner.address)

        # Log final state
        logger.info(
            "Test data generation complete",
            total_blocks=len(blockchain.chain),
            total_wallets=len(wallets),
            total_transactions=num_transactions,
        )

        return blockchain, wallets

    except Exception as e:
        logger.error("Test data generation failed", error=str(e), exc_info=True)
        raise


if __name__ == "__main__":
    generate_test_data()
