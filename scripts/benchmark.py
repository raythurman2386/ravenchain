#!/usr/bin/env python3
"""
Benchmark script for RavenChain performance testing.
Tests transaction processing, mining speed, and chain validation.
"""
import time
import statistics
from typing import List, Tuple, Dict
from config.logging import setup_logging
from ravenchain.blockchain import Blockchain
from ravenchain.wallet import Wallet

logger = setup_logging("ravenchain.benchmark")


class BlockchainBenchmark:
    def __init__(self, difficulty: int = 2):
        self.blockchain = Blockchain(difficulty=difficulty)
        self.wallet = Wallet()
        self.wallet_registry: Dict[str, Wallet] = {self.wallet.address: self.wallet}

    def benchmark_mining(self, num_blocks: int = 5) -> List[float]:
        """Benchmark mining performance."""
        mining_times = []

        for _ in range(num_blocks):
            # Add some transactions
            for _ in range(3):
                recipient = Wallet()
                self.wallet_registry[recipient.address] = recipient
                self.blockchain.add_transaction(
                    self.wallet.address, recipient.address, 1.0, wallet=self.wallet
                )

            # Time the mining process
            start_time = time.time()
            self.blockchain.mine_pending_transactions(self.wallet.address)
            mining_times.append(time.time() - start_time)

        return mining_times

    def benchmark_transaction_processing(self, num_transactions: int = 100) -> float:
        """Benchmark transaction processing speed."""
        start_time = time.time()

        for _ in range(num_transactions):
            recipient = Wallet()
            self.wallet_registry[recipient.address] = recipient
            self.blockchain.add_transaction(
                self.wallet.address, recipient.address, 1.0, wallet=self.wallet
            )

        return time.time() - start_time

    def benchmark_chain_validation(self) -> float:
        """Benchmark chain validation speed."""
        # First, create a decent-sized chain
        for _ in range(5):
            recipient = Wallet()
            self.wallet_registry[recipient.address] = recipient
            self.blockchain.add_transaction(
                self.wallet.address, recipient.address, 1.0, wallet=self.wallet
            )
            self.blockchain.mine_pending_transactions(self.wallet.address)

        # Time the validation
        start_time = time.time()
        self.blockchain.is_chain_valid(self.wallet_registry)
        return time.time() - start_time


def run_benchmarks() -> Tuple[List[float], float, float]:
    """Run all benchmarks and return results."""
    try:
        benchmark = BlockchainBenchmark()

        # Mining benchmark
        logger.info("Starting mining benchmark")
        mining_times = benchmark.benchmark_mining()
        avg_mining_time = statistics.mean(mining_times)
        logger.info(
            "Mining benchmark complete", avg_time=f"{avg_mining_time:.2f}s", times=mining_times
        )

        # Transaction processing benchmark
        logger.info("Starting transaction processing benchmark")
        tx_time = benchmark.benchmark_transaction_processing()
        logger.info(
            "Transaction benchmark complete",
            total_time=f"{tx_time:.2f}s",
            transactions_per_second=f"{100/tx_time:.2f}",
        )

        # Chain validation benchmark
        logger.info("Starting chain validation benchmark")
        validation_time = benchmark.benchmark_chain_validation()
        logger.info("Validation benchmark complete", validation_time=f"{validation_time:.2f}s")

        return mining_times, tx_time, validation_time

    except Exception as e:
        logger.error("Benchmark failed", error=str(e), exc_info=True)
        raise


if __name__ == "__main__":
    run_benchmarks()
