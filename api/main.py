from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from api.routes import block_routes, mining_routes, transaction_routes, wallet_routes, auth_routes
from api.database.models import Base
from api.dependencies import engine, logger, initialize_blockchain, limiter
from config.settings import settings
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from api.auth.utils import get_current_active_user


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


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)


@app.get("/api/health", tags=["health"])
@limiter.limit("5/minute")
async def health_check(request: Request):
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


app.include_router(auth_routes.authRouter, prefix=settings.API_PREFIX, tags=["auth"])
app.include_router(
    block_routes.blockRouter,
    prefix=settings.API_PREFIX,
    tags=["blocks"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    mining_routes.miningRouter,
    prefix=settings.API_PREFIX,
    tags=["mining"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    transaction_routes.transactionRouter,
    prefix=settings.API_PREFIX,
    tags=["transactions"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    wallet_routes.walletRouter,
    prefix=settings.API_PREFIX,
    tags=["wallets"],
    dependencies=[Depends(get_current_active_user)],
)
