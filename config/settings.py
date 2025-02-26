import os
from dotenv import load_dotenv
import secrets

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
    APP_VERSION: str = "1.0.0"
    APP_NAME: str = "RavenChain"
    APP_DESCRIPTION: str = (
        "A modern, Python-based blockchain implementation focusing on simplicity, security, and scalability."
    )
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    API_PREFIX: str = "/api/v1"
    DB_HOST = os.getenv("RAVENCHAIN_DB_HOST", "localhost")
    DB_PORT = os.getenv("RAVENCHAIN_DB_PORT", 5432)
    DB_NAME = os.getenv("RAVENCHAIN_DB_NAME", "ravenchain")
    DB_USER = os.getenv("RAVENCHAIN_DB_USER", "postgres")
    DB_PASS = os.getenv("RAVENCHAIN_DB_PASS", "admin")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # JWT Settings
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


settings = Settings()
