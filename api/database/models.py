from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base
from sqlalchemy import orm

Base = declarative_base()


class TransactionDB(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    recipient = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)
    signature = Column(LargeBinary)
    block_id = Column(Integer, ForeignKey("blocks.id"))


class BlockDB(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    index = Column(Integer, unique=True)
    timestamp = Column(DateTime, default=datetime.now)
    previous_hash = Column(String)
    nonce = Column(Integer)
    hash = Column(String)
    transactions = orm.relationship("TransactionDB", backref="block", lazy="joined")
