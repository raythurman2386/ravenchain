from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database.models import BlockDB, TransactionDB
from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with SessionLocal() as session:
    blocks = session.query(BlockDB).order_by(BlockDB.index).all()
    print(f"\nFound {len(blocks)} blocks:")
    for block in blocks:
        print(f"\nBlock {block.index}:")
        print(f"  Hash: {block.hash}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Transactions: {len(block.transactions)}")
        for tx in block.transactions:
            print(f"    - From: {tx.sender} To: {tx.recipient} Amount: {tx.amount}")
