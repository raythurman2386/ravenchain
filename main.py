from ravenchain.blockchain import Blockchain
from ravenchain.wallet import Wallet
import os
import json
import pickle
from datetime import datetime

class RavenChainCLI:
    def __init__(self):
        self.blockchain = Blockchain(difficulty=2)
        self.wallets = {}
        self.current_wallet = None
        self.wallet_file = "wallets.dat"
        self.load_wallets()

    def load_wallets(self):
        """Load saved wallets from file"""
        if os.path.exists(self.wallet_file):
            try:
                with open(self.wallet_file, 'rb') as f:
                    self.wallets = pickle.load(f)
                print("Wallets loaded successfully!")
            except:
                print("Error loading wallets. Starting fresh.")
                self.wallets = {}

    def save_wallets(self):
        """Save wallets to file"""
        with open(self.wallet_file, 'wb') as f:
            pickle.dump(self.wallets, f)
        print("Wallets saved successfully!")

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

        self.blockchain.add_transaction(sender_wallet.address, recipient, amount)
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
        print("Mining reward will be available after mining the next block.")

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
        is_valid = self.blockchain.is_chain_valid()
        print(f"\nBlockchain verification: {'VALID' if is_valid else 'INVALID'}")

    def show_menu(self):
        """Show the main menu"""
        menu = """
=== RavenChain CLI ===
1.  Create new wallet
2.  List wallets
3.  Select wallet
4.  Send RVN
5.  Mine block
6.  View blockchain
7.  View pending transactions
8.  Verify blockchain
9.  View current wallet
10. Save wallets
0.  Exit
"""
        print(menu)

    def run(self):
        """Run the CLI interface"""
        while True:
            self.show_menu()
            choice = input("Enter your choice (0-10): ").strip()

            if choice == "1":
                self.create_wallet()
            elif choice == "2":
                self.list_wallets()
            elif choice == "3":
                self.select_wallet()
            elif choice == "4":
                self.send_transaction()
            elif choice == "5":
                self.mine_block()
            elif choice == "6":
                self.view_blockchain()
            elif choice == "7":
                self.view_pending_transactions()
            elif choice == "8":
                self.verify_blockchain()
            elif choice == "9":
                if self.current_wallet:
                    self.print_wallet_info(self.wallets[self.current_wallet], self.current_wallet)
                else:
                    print("No wallet selected!")
            elif choice == "10":
                self.save_wallets()
            elif choice == "0":
                print("Thank you for using RavenChain!")
                break
            else:
                print("Invalid choice! Please try again.")

            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')

def main():
    cli = RavenChainCLI()
    cli.run()

if __name__ == "__main__":
    main()