from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlalchemy import inspect, text
from api.routes import block_routes, mining_routes, transaction_routes, wallet_routes
from api.database.models import Base
from api.dependencies import engine, logger, initialize_blockchain


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application")
    try:
        if not inspect(engine).has_table("blocks"):
            logger.info("Creating database tables")
            Base.metadata.create_all(engine)
        # Initialize blockchain
        initialize_blockchain()
        logger.info("Application startup complete")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        # Shutdown: Properly close all resources
        logger.info("Shutting down application")
        try:
            engine.dispose()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error disposing engine: {str(e)}")


app = FastAPI(lifespan=lifespan)


@app.get("/api/health", tags=["health"])
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


app.include_router(block_routes.blockRouter, prefix="/api/v1", tags=["blocks"])
app.include_router(mining_routes.miningRouter, prefix="/api/v1", tags=["mining"])
app.include_router(transaction_routes.transactionRouter, prefix="/api/v1", tags=["transactions"])
app.include_router(wallet_routes.walletRouter, prefix="/api/v1", tags=["wallets"])
