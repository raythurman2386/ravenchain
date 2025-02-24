import os
from dotenv import load_dotenv

load_dotenv()
MINING_DIFFICULTY = 4
MINING_REWARD = 10.0
BLOCK_TIME_TARGET = 600  # Target time between blocks in seconds (10 minutes like Bitcoin)

# Network configuration
NODE_PORT = 5000
PEERS = []  # List of peer nodes

# Wallet configuration
WALLET_PATH = "wallet.dat"


class Settings:
    DB_HOST = os.getenv("RAVENCHAIN_DB_HOST", "localhost")
    DB_PORT = os.getenv("RAVENCHAIN_DB_PORT", 5432)
    DB_NAME = os.getenv("RAVENCHAIN_DB_NAME", "ravenchain")
    DB_USER = os.getenv("RAVENCHAIN_DB_USER", "postgres")
    DB_PASS = os.getenv("RAVENCHAIN_DB_PASS", "admin")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = Settings()
