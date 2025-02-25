from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from config.logging import setup_logging
from ravenchain import Blockchain
import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a single limiter instance to be shared across the application
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])


# Setup logging
logger = setup_logging(
    "ravenchain.api", json_output=os.getenv("LOG_JSON", "0") == "1", console_output=True
)

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize blockchain
blockchain = None


def initialize_blockchain():
    """Initialize the blockchain with the database session"""
    global blockchain
    if blockchain is None:
        logger.info("Initializing blockchain")
        blockchain = Blockchain(SessionLocal)
    return blockchain


def get_blockchain():
    """Get the blockchain instance, initializing it if necessary"""
    if blockchain is None:
        return initialize_blockchain()
    return blockchain
