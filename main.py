import os
import json
import pickle
from pathlib import Path
from datetime import datetime
from ravenchain.blockchain import Blockchain
from ravenchain.wallet import Wallet
from config.logging import setup_logging

logger = setup_logging(
    "ravenchain.cli", json_output=os.getenv("LOG_JSON", "0") == "1", console_output=True
)


class RavenChainCLI:
    def __init__(self):
        self.data_dir = Path(os.getenv("RAVENCHAIN_DATA_DIR", "data"))
        self.difficulty = int(os.getenv("MINING_DIFFICULTY", "2"))
        self.debug = os.getenv("DEBUG", "0") == "1"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.blockchain = Blockchain(difficulty=self.difficulty)
        self.wallets = {}
        self.current_wallet = None
        self.wallet_file = self.data_dir / "wallets.dat"

        if self.debug:
            logger.setLevel("DEBUG")

        logger.info(
            "Initializing RavenChain CLI",
            data_dir=str(self.data_dir),
            difficulty=self.difficulty,
            debug=self.debug,
        )
        self.load_wallets()

    def load_wallets(self):
        """Load saved wallets from file"""
        if self.wallet_file.exists():
            try:
                with open(self.wallet_file, "rb") as f:
                    self.wallets = pickle.load(f)
                logger.info("Wallets loaded successfully", wallet_count=len(self.wallets))
            except Exception as e:
                logger.error(
                    "Error loading wallets", error=str(e), wallet_file=str(self.wallet_file)
                )
                self.wallets = {}
        else:
            logger.info("No wallet file found. Starting fresh", wallet_file=str(self.wallet_file))

    def save_wallets(self):
        """Save wallets to file"""
        try:
            with open(self.wallet_file, "wb") as f:
                pickle.dump(self.wallets, f)
            logger.info(
                "Wallets saved successfully",
                wallet_count=len(self.wallets),
                wallet_file=str(self.wallet_file),
            )
        except Exception as e:
            logger.error("Error saving wallets", error=str(e), wallet_file=str(self.wallet_file))

    def print_wallet_info(self, wallet, name=""):
        """Print wallet details"""
        balance = self.blockchain.get_balance(wallet.address)
        print(f"\nWallet{f' {name}' if name else ''}")
        print(f"Address: {wallet.address}")
        print(f"Balance: {balance} RVN")

    def create_wallet(self):
        """Create a new wallet"""
        name = input("Enter wallet name: ").strip()
        if name in self.wallets:
            print("Wallet with this name already exists!")
            return

        wallet = Wallet()
        self.wallets[name] = wallet
        self.save_wallets()
        print(f"\nWallet '{name}' created successfully!")
        self.print_wallet_info(wallet, name)

    def list_wallets(self):
        """List all wallets"""
        if not self.wallets:
            print("No wallets found. Create one first!")
            return

        print("\n=== Wallets ===")
        for name, wallet in self.wallets.items():
            self.print_wallet_info(wallet, name)

    def select_wallet(self):
        """Select a wallet to use"""
        if not self.wallets:
            print("No wallets found. Create one first!")
            return

        print("\nAvailable wallets:")
        for name in self.wallets:
            print(f"- {name}")

        name = input("\nEnter wallet name to select: ").strip()
        if name in self.wallets:
            self.current_wallet = name
            print(f"Selected wallet: {name}")
            self.print_wallet_info(self.wallets[name], name)
        else:
            print("Wallet not found!")

    def send_transaction(self):
        """Send RVN to another address"""
        if not self.current_wallet:
            print("No wallet selected! Select a wallet first.")
            return

        recipient = input("Enter recipient address: ").strip()
        try:
            amount = float(input("Enter amount to send: ").strip())
        except ValueError:
            print("Invalid amount!")
            return

        sender_wallet = self.wallets[self.current_wallet]
        if self.blockchain.get_balance(sender_wallet.address) < amount:
            print("Insufficient balance!")
            return

        self.blockchain.add_transaction(
            sender_wallet.address, recipient, amount, wallet=sender_wallet
        )
        print("Transaction added to pending pool!")
        print("Mine a new block to confirm the transaction.")

    def mine_block(self):
        """Mine a new block"""
        if not self.current_wallet:
            print("No wallet selected! Select a wallet first.")
            return

        print("Mining new block...")
        self.blockchain.mine_pending_transactions(self.wallets[self.current_wallet].address)
        print("Block mined successfully!")
        print("Mining reward added to your wallet.")

    def view_blockchain(self):
        """View all blocks in the blockchain"""
        print("\n=== Blockchain Data ===")
        for block in self.blockchain.chain:
            print(f"\nBlock #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            if isinstance(block.data, list):
                print("Transactions:")
                for tx in block.data:
                    print(f"  From: {tx.sender or 'Mining Reward'}")
                    print(f"  To: {tx.recipient}")
                    print(f"  Amount: {tx.amount} RVN")
            print("-" * 50)

    def view_pending_transactions(self):
        """View all pending transactions"""
        if not self.blockchain.pending_transactions:
            print("No pending transactions.")
            return

        print("\n=== Pending Transactions ===")
        for tx in self.blockchain.pending_transactions:
            print(f"\nFrom: {tx.sender or 'Mining Reward'}")
            print(f"To: {tx.recipient}")
            print(f"Amount: {tx.amount} RVN")
            print(f"Timestamp: {tx.timestamp}")

    def verify_blockchain(self):
        """Verify blockchain integrity"""
        wallet_registry = {wallet.address: wallet for wallet in self.wallets.values()}
        is_valid = self.blockchain.is_chain_valid(wallet_registry)
        print(f"\nBlockchain verification: {'VALID' if is_valid else 'INVALID'}")

    def view_current_wallet(self):
        """View current wallet"""
        if self.current_wallet:
            self.print_wallet_info(self.wallets[self.current_wallet], self.current_wallet)
        else:
            print("No wallet selected!")


def main():
    try:
        logger.info(
            "Starting RavenChain node",
            data_dir=os.getenv("RAVENCHAIN_DATA_DIR", "data"),
            mining_difficulty=os.getenv("MINING_DIFFICULTY", "2"),
            debug=os.getenv("DEBUG", "0"),
            version="1.0.0",
        )

        cli = RavenChainCLI()
        while True:
            print("\n=== RavenChain CLI ===")
            print("1. Create new wallet")
            print("2. List wallets")
            print("3. Select wallet")
            print("4. Send RVN")
            print("5. Mine block")
            print("6. View blockchain")
            print("7. View pending transactions")
            print("8. Verify blockchain")
            print("9. View current wallet")
            print("10. Save wallets")
            print("0. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "0":
                logger.info("Shutting down RavenChain node")
                break

            # Map choices to methods
            actions = {
                "1": cli.create_wallet,
                "2": cli.list_wallets,
                "3": cli.select_wallet,
                "4": cli.send_transaction,
                "5": cli.mine_block,
                "6": cli.view_blockchain,
                "7": cli.view_pending_transactions,
                "8": cli.verify_blockchain,
                "9": cli.view_current_wallet,
                "10": cli.save_wallets,
            }

            if choice in actions:
                try:
                    logger.debug(f"Executing action", action=choice)
                    actions[choice]()
                except Exception as e:
                    logger.error(
                        "Error executing action", action=choice, error=str(e), exc_info=True
                    )
                    if cli.debug:
                        raise
            else:
                logger.warning("Invalid choice entered", choice=choice)
                print("Invalid choice!")

    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error("Unexpected error", error=str(e), exc_info=True)
        raise
    finally:
        # Ensure wallets are saved on exit
        if "cli" in locals():
            cli.save_wallets()
        logger.info("RavenChain node stopped")


if __name__ == "__main__":
    main()
